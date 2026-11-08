import socket, threading

clients = {}  # Store socket -> name mapping

def handle(client, addr):
    name = client.recv(1024).decode().strip()
    clients[client] = name
    print(f"{name} Connected")

    while True:
        try:
            msg = client.recv(1024)
            if not msg: break
            
            formatted_msg = f"{name}: {msg.decode()}"
            print(formatted_msg)  # Prints on server terminal
            
            # Broadcast to all other clients
            [c.sendall(formatted_msg.encode()) for c in clients if c != client]
        except: break
        
    print(f"{name} Disconnected")
    clients.pop(client, None)
    client.close()

with socket.create_server(("127.0.0.1", 12345)) as server:
    print("Chat server running...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle, args=(client, addr), daemon=True).start()