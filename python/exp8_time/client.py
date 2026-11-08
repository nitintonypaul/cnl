import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
	sock.sendto(b"TIME", ("127.0.0.1", 12345))
	data, _ = sock.recvfrom(1024)
	print(f"Current Server Time:\n{data.decode()}")