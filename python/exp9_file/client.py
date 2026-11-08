import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
	fname = input("Enter filename to request: ")
	sock.sendto(fname.encode(), ("127.0.0.1", 12345))

	data, _ = sock.recvfrom(1024)
	print(f"\nResponse from Server:\n{data.decode()}")
