#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <net/ethernet.h>

int main() {
    int sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sock < 0) {
        perror("Socket Error (Did you run with sudo?)");
        return 1;
    }

    unsigned char buffer[65536];
    printf("C Packet Sniffer started...\n");

    while (1) {
        int data_size = recvfrom(sock, buffer, sizeof(buffer), 0, NULL, NULL);
        if (data_size < 0) continue;

        struct ether_header *eth = (struct ether_header *)buffer;
        printf("\n[Ethernet] Proto: %#06x\n", ntohs(eth->ether_type));

        // Check if IPv4 (0x0800)
        if (ntohs(eth->ether_type) == 0x0800) {
            struct iphdr *ip = (struct iphdr *)(buffer + sizeof(struct ether_header));
            
            struct sockaddr_in src, dest;
            memset(&src, 0, sizeof(src));
            memset(&dest, 0, sizeof(dest));
            src.sin_addr.s_addr = ip->saddr;
            dest.sin_addr.s_addr = ip->daddr;

            printf("  [IPv4] %s -> %s | Protocol: %d | TTL: %d\n", 
                   inet_ntoa(src.sin_addr), 
                   inet_ntoa(dest.sin_addr), 
                   ip->protocol, 
                   ip->ttl);
        }
    }
    close(sock);
    return 0;
}
