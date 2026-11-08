import socket, time

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
	server.bind(("127.0.0.1", 12345))
	print("UDP Time Server running...")
	while True:
		_, addr = server.recvfrom(1024)

		current_time = time.ctime().encode()
		server.sendto(current_time, addr)

		print("Time request served.")
