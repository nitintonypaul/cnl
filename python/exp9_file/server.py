import socket, threading, os

def handle_request(server_sock, addr, filename):
    # --------------------------------------------------
    # CORE LOGIC: Read file content, attach thread/process ID, send response
    pid = os.getpid()
    response = f"Handled by Server ID (PID/Thread): {pid}\n\n"
    
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, "r") as f:
            response += f.read()
    else:
        response += "Requested File Not Found."
        
    server_sock.sendto(response.encode(), addr)
    print(f"Served file '{filename}' to {addr}")
    # --------------------------------------------------

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind(("127.0.0.1", 12345))
    print("UDP Concurrent File Server running...")
    
    while True:
        data, addr = server.recvfrom(1024)
        filename = data.decode().strip()
        
        # Spawn a concurrent thread for each client request
        threading.Thread(target=handle_request, args=(server, addr, filename), daemon=True).start()