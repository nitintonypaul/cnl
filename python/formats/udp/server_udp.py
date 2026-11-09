import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind(("127.0.0.1", 12345))
    data, addr = server.recvfrom(1024)
    data = data.decode()

    # Do something with the data
    data = "Done something with the data"

    server.sendto(data.encode(), addr)
