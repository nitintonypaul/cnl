import socket

# Create server with this specific address and port number
with socket.create_server(("127.0.0.1", 12345)) as server:

    # Accept a client
    client, _ = server.accept()

    # using the said client
    with client:

        # Recieve data from client. No address is passed
        data = client.recv(1024).decode()

        # Do something with the data
        data = "Done something with the data"

        # Send the response back to the client
        client.sendall(data.encode())