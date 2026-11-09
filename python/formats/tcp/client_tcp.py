import socket

# Create connection to this specific address
with socket.create_connection(("127.0.0.1", 12345)) as sock:

    # Obtain data
    data = input("> ")

    # Send data to server
    sock.sendall(data.encode())

    # Recieve response
    # Use buffer size 1024 for exam. It is enough
    res = sock.recv(1024).decode()

    # Do something with the response
    print(res)