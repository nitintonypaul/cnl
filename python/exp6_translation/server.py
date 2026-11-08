import socket

mapping = {
    "tbh": "to be honest", "ig": "I guess", "tbf": "to be fair",
    "atm": "at the moment", "irl": "in real life", "lol": "laughing out loud",
    "asap": "as soon as possible", "omg": "oh my God", "ttyl": "talk to you later",
    "idk": "I don't know", "nvm": "never mind", "idc": "I don't care"
}

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind(("127.0.0.1", 12345))
    print("UDP server waiting...")
    data, addr = server.recvfrom(1024)
    words = data.decode().split()
    translated = " ".join([mapping.get(w.lower(), w) for w in words])
    server.sendto(translated.encode(), addr)
    