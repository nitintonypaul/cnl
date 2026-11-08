import socket
import struct

# Create raw socket to capture all incoming Ethernet frames (ETH_P_ALL = 0x0003)
with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as conn:
    print("Full Packet Sniffer started... Press Ctrl+C to stop.")
    
    while True:
        raw_data, _ = conn.recvfrom(65536)
        
        # 1. Ethernet Header (14 bytes)
        eth_header = raw_data[:14]
        dest_mac, src_mac, eth_proto = struct.unpack("! 6s 6s H", eth_header)
        
        dest_str = ":".join(f"{b:02x}" for b in dest_mac)
        src_str = ":".join(f"{b:02x}" for b in src_mac)
        protocol_type = socket.htons(eth_proto)
        
        print(f"\n[Ethernet] Src: {src_str} | Dest: {dest_str} | Proto: {protocol_type:#06x}")
        
        # 2. Check if IPv4 (0x0800)
        if protocol_type == 0x0800:
            ip_header = raw_data[14:34]
            # Unpack IPv4 header fields
            version_ihl, _, _, _, _, _, ttl, proto, _, src_ip, dest_ip = struct.unpack("! B B H H H b b H 4s 4s", ip_header)
            
            ihl = (version_ihl & 0x0F) * 4  # Calculate IP header length in bytes
            src_addr = socket.inet_ntoa(src_ip)
            dest_addr = socket.inet_ntoa(dest_ip)
            
            print(f"  [IPv4] {src_addr} -> {dest_addr} | TTL: {ttl} | Protocol Number: {proto}")
            
            # 3. Transport Layer Parsing based on Protocol Number
            transport_start = 14 + ihl
            
            # TCP (Protocol 6)
            if proto == 6:
                tcp_header = raw_data[transport_start:transport_start+20]
                src_port, dest_port, _, _, _, _, _, _, _ = struct.unpack("! H H L L H H H H H", tcp_header)
                print(f"    [TCP] Port {src_port} -> Port {dest_port}")
                
            # UDP (Protocol 17)
            elif proto == 17:
                udp_header = raw_data[transport_start:transport_start+8]
                src_port, dest_port, length, checksum = struct.unpack("! H H H H", udp_header)
                print(f"    [UDP] Port {src_port} -> Port {dest_port} | Length: {length}")
                
            # ICMP (Protocol 1)
            elif proto == 1:
                icmp_header = raw_data[transport_start:transport_start+4]
                icmp_type, code, checksum = struct.unpack("! B B H", icmp_header)
                print(f"    [ICMP] Type: {icmp_type} | Code: {code}")
