import socket, threading

sock = socket.create_connection(("127.0.0.1", 12345))
name = input("Enter your name: ")
sock.sendall(name.encode())

# Background thread to receive and print incoming messages
threading.Thread(target=lambda: [print(sock.recv(1024).decode()) for _ in iter(int, 1)], daemon=True).start()

while True:
    msg = input("> ")
    sock.sendall(msg.encode())