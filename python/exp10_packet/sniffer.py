import socket
import struct

with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as conn:
    print("Packet Sniffer started... Press Ctrl+C to stop.")
    
    while True:
        raw_data, _ = conn.recvfrom(65536)
        eth_header = raw_data[:14]
        dest_mac, src_mac, eth_proto = struct.unpack("! 6s 6s H", eth_header)
        
        dest_str = ":".join(f"{b:02x}" for b in dest_mac)
        src_str = ":".join(f"{b:02x}" for b in src_mac)
        
        print(f"\n[Ethernet] Src: {src_str} | Dest: {dest_str} | Protocol: {socket.htons(eth_proto):#06x}")
        
        if socket.htons(eth_proto) == 0x0800:
            ip_header = raw_data[14:34]
            version_ihl, _, _, _, _, _, ttl, proto, _, src_ip, dest_ip = struct.unpack("! B B H H H b b H 4s 4s", ip_header[:20])
            
            src_addr = socket.inet_ntoa(src_ip)
            dest_addr = socket.inet_ntoa(dest_ip)
            
            proto_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
            protocol_name = proto_map.get(proto, f"OTHER({proto})")
            
            print(f"  [IPv4] {src_addr} -> {dest_addr} | Protocol: {protocol_name} | TTL: {ttl}")
        # --------------------------------------------------