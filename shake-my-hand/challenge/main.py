#!/usr/bin/env python3

import base64
import random
import readline
import secrets
import threading
import time

from scapy.all import *

# Some constants to make it easier to read.
AWAITING_ACK = 0
ESTABLISHED  = 1

SERVER_IP = "192.168.1.10"
SERVER_PORT = 9999

# Tick time in seconds.
DT = 0.1

# Helps ^C close the threads.
KILL = False

# Client FIFO buffer for packets being received.
recvBuffer = []
recvLock = threading.Lock()

# Client FIFO buffer for packets being emitted.
emitBuffer = []
emitLock = threading.Lock()

def _emit_push(packet: bytes):

	emitLock.acquire()
	global emitBuffer
	emitBuffer.append(packet)
	emitLock.release()

def _emit_pop() -> bytes:

	emitLock.acquire()
	global emitBuffer

	if len(emitBuffer) == 0:
		emitLock.release()
		return None
	packet = emitBuffer.pop(0)

	emitLock.release()
	return packet

def _recv_push(packet: bytes):

	recvLock.acquire()
	global recvBuffer
	recvBuffer.append(packet)
	recvLock.release()

def _recv_pop(ip: str) -> bytes:

	recvLock.acquire()
	global recvBuffer

	packet = IP()

	# Filter out everything not addressed to user host.
	while packet.dst != ip:
		if len(recvBuffer) == 0:
			recvLock.release()
			return None
		packet = IP(recvBuffer.pop(0))

	recvLock.release()
	return bytes(packet)

def emit(cmd: str):

	tokens = cmd.split()

	if len(tokens) != 2:
		print("Error: invalid command.")
		return

	try:
		packet = base64.b64decode(tokens[1])
	except:
		print("Error: could not decode packet from base64.")
		return

	print("Adding packet to emit buffer... ", end="")
	_emit_push(packet)
	print("done.")

def recv(ip: str, cmd: str):

	print("Retrieving packet from receive buffer... ", end="")
	packet = _recv_pop(ip)
	print("done.")

	if not packet:
		print("recv buffer is empty.")
		return

	print(base64.b64encode(packet).decode())

def help():

	print()
	print("  Commands")
	print("    help, ?       - Show this help message.")
	print("    exit          - Quit the simulator.")
	print("    emit <packet> - Emit a base64-encoded packet.")
	print("    recv          - Receive a base64-encoded packet.")
	print()

def sim_server(ip: str, port: int):

	memory = {}  # {(clientIp, clientPort): {"state": s, "x": x, "y": y}, ...}

	while not KILL:

		time.sleep(DT)
		packet = _emit_pop()
		if not packet:
			continue

		# We only care about TCP packets for this challenge.
		try:
			packet = IP(packet)
			tcp = packet[TCP]
		except:
			continue

		# We only care about packets addressed to us.
		if packet.dst != ip:
			continue

		# We're only listening on the specified port.
		if tcp.dport != port:
			continue

		clientIp = packet.src
		clientPort = tcp.sport

		k = (clientIp, clientPort)

		# New connection starting the handshake. Receive syn, reply syn+ack.
		if k not in memory.keys():
			if not tcp.flags == "S":
				continue
			x = tcp.seq
			y = secrets.randbits(32)
			p = IP(src=ip, dst=clientIp) \
				/ TCP(dport=clientPort, sport=port, flags="SA", seq=y, ack=x+1)
			_recv_push(bytes(p))
			memory[k] = {"state": AWAITING_ACK, "x": x, "y": y}

		# Finishing the handshake. Receive ack. Send psh+ack.
		elif k in memory.keys() and memory[k]["state"] == AWAITING_ACK:
			if not tcp.flags == "A":
				continue
			if tcp.seq != memory[k]["x"]+1:
				continue
			if tcp.ack != memory[k]["y"]+1:
				continue
			memory[k] = {"state": ESTABLISHED, "x": tcp.seq, "y": tcp.ack}
			p = IP(src=ip, dst=clientIp) \
				/ TCP(dport=clientPort, sport=port, flags="PA", seq=memory[k]["y"], ack=memory[k]["x"]) \
				/ b"Print flag? [yes|no]\n"
			_recv_push(bytes(p))
			memory[k] = {"state": ESTABLISHED, "x": tcp.seq, "y": tcp.ack+len(p[TCP].payload)}

		# Connection established.
		elif k in memory.keys() and memory[k]["state"] == ESTABLISHED:
			if not tcp.flags in ("A", "PA"):
				continue
			if tcp.seq != memory[k]["x"]:
				continue
			if tcp.flags == "A" and tcp.ack != memory[k]["y"]:
				continue
			if tcp.flags == "PA":
				if tcp.ack != memory[k]["y"]:
					continue
				length = len(tcp.payload)
				memory[k] = {"state": ESTABLISHED, "x": tcp.seq+length, "y": tcp.ack}
				if bytes(tcp.payload).decode().strip() == "yes":
					p = IP(src=ip, dst=clientIp) \
						/ TCP(dport=clientPort, sport=port, flags="PA", seq=memory[k]["y"], ack=memory[k]["x"]) \
						/ b"irisctf{tcp_h4ndsh4k35_are_a_br33ze_1n_th3_p4rk}\n"
					_recv_push(bytes(p))
					endLength = len(p[TCP].payload)
				else:
					p = IP(src=ip, dst=clientIp) \
						/ TCP(dport=clientPort, sport=port, flags="PA", seq=memory[k]["y"], ack=memory[k]["x"]) \
						/ b"Response not 'yes'. Exiting.\n"
					_recv_push(bytes(p))
					endLength = len(p[TCP].payload)
				p = IP(src=ip, dst=clientIp) \
					/ TCP(dport=clientPort, sport=port, flags="R", seq=memory[k]["y"]+endLength, ack=memory[k]["x"])
				_recv_push(bytes(p))

def main():

	userIp = f"192.168.1.{random.randint(11, 254)}"

	t1 = threading.Thread(target=sim_server, args=(SERVER_IP, SERVER_PORT),
		daemon=True).start()

	print("--[ Network Simulator ]-----------------------------------------------")
	print("This network simulator is not a part of the challenge. This just helps")
	print("you complete the challenge without upsetting your network admin.")
	print()
	print(f"Challenge IP: {SERVER_IP}")
	print(f"Challenge Port: {SERVER_PORT}/tcp")
	print()
	print(f"Your IP: {userIp}")
	print()
	print("--[ Layer 3 ]---------------------------------------------------------")
	help()

	try:
		while True:
			cmd = str(input("> ").strip())
			assert len(cmd) < 1024  # no packet should be this large.
			if cmd == "":
				pass
			elif cmd in ("help", "?"):
				help()
			elif cmd.startswith("emit "):
				emit(cmd)
			elif cmd == "recv":
				recv(userIp, cmd)
			elif cmd == "exit":
				break
			else:
				print("Error: invalid command.")
	except KeyboardInterrupt:
		print("\nInterrupted.")
	except:
		print("Fatal error. Aborting.")

	global KILL
	KILL = True
	print("Exiting.")

main()
