import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

    # Input some value
    data = input("> ")
    sock.sendto(data.encode(), ("127.0.0.1", 12345))

    # Obtain response
    data, _ = sock.recvfrom(1024)

    print(data.decode())