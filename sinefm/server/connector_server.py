#!/usr/bin/env python3

# Servers:
# udp/6530 - receive IQ data from the local GRC flow.
# udp/7821 - receive IQ data from the interrupt stream. This should ideally be
#            over an SSH tunnel to prevent radio piracy over IP.
# tcp/6531 - send IQ data to kCTF servers.

import socket
import threading

UDP_SERVER = ("localhost", 6530)
TCP_SERVER = ("0.0.0.0", 6531)
INTERRUPT_UDP_SERVER = ("0.0.0.0", 7821)

clients = {}
lock = threading.Lock()

transmitLock = threading.Lock()

def get_clients():
	lock.acquire()
	global clients
	c = clients.copy()
	lock.release()
	return c

def add_client(ip, port, sock):
	lock.acquire()
	global clients
	addr = (ip, port)
	print(f"Adding client: {addr}")
	clients[addr] = sock
	lock.release()

def remove_client(ip, port):
	lock.acquire()
	global clients
	addr = (ip, port)
	print(f"Removing client: {addr}")
	del clients[addr]
	lock.release()

def udp_listener(grcSock):

	while True:
		transmitLock.acquire()
		data, addr = grcSock.recvfrom(1472)
		for client in get_clients().values():
			try:
				client.send(data)
			except:
				pass
		transmitLock.release()

def interrupt_listener(interruptSock):

	interruptSock.settimeout(1)

	while True:
		try:
			data, addr = interruptSock.recvfrom(1472)
		except socket.timeout:
			continue
		if not data:
			continue
		transmitLock.acquire()
		try:
			while data:
				for client in get_clients().values():
					try:
						client.send(data)
					except:
						pass
				try:
					data, addr = interruptSock.recvfrom(1472)
				except socket.timeout:
					break
		finally:
			transmitLock.release()

def handle_client(sock, ip, port):
	try:
		while True:
			data = sock.recv(1024)
	except Exception as e:
		print(f"({ip}:{port}) Error: {e}")
	finally:
		remove_client(ip, port)
		sock.close()

def main():

	print("Starting.")

	# Listening for data from the local GRC flow.
	grcUdpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	grcUdpSock.bind(UDP_SERVER)
	threading.Thread(target=udp_listener, args=(grcUdpSock,)).start()
	print(f"Listening on {UDP_SERVER} (UDP) for data from the local GRC flow.")

	# Listening for connections from the interrupt server.
	interruptSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	interruptSock.bind(INTERRUPT_UDP_SERVER)
	threading.Thread(target=interrupt_listener, args=(interruptSock,)).start()
	print(f"Listening on {INTERRUPT_UDP_SERVER} (UDP) for interrupt connections.")

	# Listening for clients to connect. The only clients should be kCTF servers
	# who have their own middleware to serve it to users.
	tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpSock.bind(TCP_SERVER)
	print(f"Listening on {TCP_SERVER} (TCP) for kCTF servers.")
	tcpSock.listen(128)

	while True:
		sock, addr = tcpSock.accept()
		threading.Thread(target=handle_client, args=(sock, addr[0], addr[1])).start()
		add_client(addr[0], addr[1], sock)

main()
