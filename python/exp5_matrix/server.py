import socket, json

with socket.create_server(("127.0.0.1", 12345)) as server:
    print("Server waiting...")
    client, _ = server.accept()
    with client:
        d = json.loads(client.recv(4096).decode())
        N, m = d["N"], d["mat"]
        
        up = all(m[i][j] == 0 for i in range(N) for j in range(N) if i > j)
        low = all(m[i][j] == 0 for i in range(N) for j in range(N) if i < j)
        diag = all(m[i][j] == 0 for i in range(N) for j in range(N) if i != j)
        
        res = "Diagonal" if diag else "Upper Triangular" if up else "Lower Triangular" if low else "Not Special"
        client.sendall(res.encode())