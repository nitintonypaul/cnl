import socket, json, random

with socket.create_connection(("127.0.0.1", 12345)) as sock:
    N = int(input("Enter N: "))
    matrix = [[random.randint(0, 50) for _ in range(N)] for _ in range(N)]
    sock.sendall(json.dumps({"N": N, "mat": matrix}).encode())
    print("Matrix:\n")
    for i in matrix:
        print(i) 
    print(f"Result: {sock.recv(1024).decode()}")