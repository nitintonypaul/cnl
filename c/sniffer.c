#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ip_icmp.h>

int main() {
    int sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sockfd < 0) { perror("Socket"); return 1; }

    unsigned char *buffer = malloc(65536);
    printf("C Packet Sniffer running (Press Ctrl+C to stop)...\n");

    while (1) {
        int data_size = recvfrom(sockfd, buffer, 65536, 0, NULL, NULL);
        if (data_size < 0) break;

        struct ethhdr *eth = (struct ethhdr *)buffer;
        unsigned short proto = ntohs(eth->h_proto);
        
        printf("\n[Eth] Src: %02X:%02X:%02X:%02X:%02X:%02X -> Dst: %02X:%02X:%02X:%02X:%02X:%02X | Proto: 0x%04X",
               eth->h_source[0], eth->h_source[1], eth->h_source[2], eth->h_source[3], eth->h_source[4], eth->h_source[5],
               eth->h_dest[0], eth->h_dest[1], eth->h_dest[2], eth->h_dest[3], eth->h_dest[4], eth->h_dest[5], proto);

        if (proto == ETH_P_IP) {
            struct iphdr *iph = (struct iphdr *)(buffer + sizeof(struct ethhdr));
            struct in_addr src = {iph->saddr}, dst = {iph->daddr};
            
            printf("\n  [IP] %s -> %s | TTL: %d | Proto: %d", 
                   inet_ntoa(src), inet_ntoa(dst), iph->ttl, iph->protocol);

            unsigned char *transport = buffer + sizeof(struct ethhdr) + (iph->ihl * 4);

            if (iph->protocol == IPPROTO_TCP) {
                struct tcphdr *tcp = (struct tcphdr *)transport;
                printf("\n    [TCP] Port %u -> %u", ntohs(tcp->source), ntohs(tcp->dest));
            } 
            else if (iph->protocol == IPPROTO_UDP) {
                struct udphdr *udp = (struct udphdr *)transport;
                printf("\n    [UDP] Port %u -> %u", ntohs(udp->source), ntohs(udp->dest));
            } 
            else if (iph->protocol == IPPROTO_ICMP) {
                struct icmphdr *icmp = (struct icmphdr *)transport;
                printf("\n    [ICMP] Type: %d | Code: %d", icmp->type, icmp->code);
            }
        }
    }
    close(sockfd);
    free(buffer);
    return 0;
}
