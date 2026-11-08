import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
	msg = input("Enter sentence: ")
	sock.sendto(msg.encode(), ("127.0.0.1", 12345))
	data, _ = sock.recvfrom(1024)
	print(f"\nTranslated: {data.decode()}")
