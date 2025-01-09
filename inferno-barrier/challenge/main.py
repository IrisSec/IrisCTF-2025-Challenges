#!/usr/bin/env python3

import base64
import random
import readline
import threading
import time

from scapy.all import *

SERVER_IP = "192.168.1.10"
SERVER_PORT = 4545

ALLOWED_IP = "192.168.1.4"

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

def _recv_pop(promiscuous: bool, ip: str) -> bytes:

	recvLock.acquire()
	global recvBuffer

	packet = IP()

	while packet.dst != ip:
		if len(recvBuffer) == 0:
			recvLock.release()
			return None
		packet = IP(recvBuffer.pop(0))
		if promiscuous:
			break

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

def recv(promiscuous: bool, ip: str, cmd: str):

	print("Retrieving packet from receive buffer... ", end="")
	packet = _recv_pop(promiscuous, ip)
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
	print("    prom <on|off> - Turn promiscuous mode on or off.")
	print()

def sim_server(ip: str, port: int):

	n = -20
	announcement = None  # "generic" | "date" | "time" | "flag"

	while not KILL:

		n += 1

		# Announcement broadcast every 10 seconds.
		if n % 100 == 0:
			if announcement == None:
				message = b"Announcement: error: no announcement configured.\n" \
				  b"Run 'select (generic|date|time|flag)' to configure.\n"
			elif announcement == "generic":
				message = b"Announcement: Greetings!\n"
			elif announcement == "date":
				message = time.strftime("Announcement: Today is %m-%d-%Y.\n").encode()
			elif announcement == "time":
				message = time.strftime("Announcement: The time is %H:%M:%S.\n").encode()
			elif announcement == "flag":
				message = b"Announcement: irisctf{udp_1p_sp00fing_is_tr1vial_but_un1dir3ct10nal}\n"

			p = IP(src=ip, dst=ALLOWED_IP) \
				/ UDP(sport=port, dport=10343) \
				/ message
			_recv_push(bytes(p))

		time.sleep(DT)
		packet = _emit_pop()
		if not packet:
			continue

		# We only care about UDP packets for this challenge.
		try:
			packet = IP(packet)
			udp = packet[UDP]
		except:
			continue

		# We only care about packets addressed to us on the listening port.
		if (packet.dst != ip) or (udp.dport != port):
			continue

		clientIp = packet.src
		clientPort = udp.sport

		# We only care about packets from the allowed IP.
		if clientIp != ALLOWED_IP:
			print(f"\n<Firewall: (drop) {clientIp}:{clientPort} -> {ip}:{port}" \
				" due to policy: allow-192-168-1-4-only>")
			continue

		# Get and parse the payload.
		payload = bytes(udp.payload).decode().strip()
		if payload == "select generic":
			announcement = "generic"
		elif payload == "select date":
			announcement = "date"
		elif payload == "select time":
			announcement = "time"
		elif payload == "select flag":
			announcement = "flag"

def main():

	userIp = f"192.168.1.{random.randint(11, 254)}"

	t1 = threading.Thread(target=sim_server, args=(SERVER_IP, SERVER_PORT),
		daemon=True).start()

	# Completing the challenge premise IRL can outright be a felony lmao
	print("--[ Network Simulator ]-----------------------------------------------")
	print("This network simulator is not a part of the challenge. This just helps")
	print("you complete the challenge without upsetting your network admin.")
	print()
	print(f"Your IP: {userIp}")
	print()
	print("--[ Layer 3 ]---------------------------------------------------------")
	help()

	try:
		prom = False
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
				recv(prom, userIp, cmd)
			elif cmd == "exit":
				break
			elif cmd == "prom on":
				prom = True
				print("Promiscuous mode enabled.")
			elif cmd == "prom off":
				prom = False
				print("Promiscuous mode disabled.")
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
