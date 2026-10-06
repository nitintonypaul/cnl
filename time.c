// This program is for the server

#include<stdio.h>
#include<string.h>
#include<time.h>
#include<arpa/inet.h>

int main()
{
    int s=socket(AF_INET,SOCK_DGRAM,0);
    struct sockaddr_in sa,ca;
    socklen_t l=sizeof(ca);
    char b[100];
    time_t t;

    sa.sin_family=AF_INET;
    sa.sin_addr.s_addr=INADDR_ANY;
    sa.sin_port=htons(9000);
    bind(s,(struct sockaddr*)&sa,sizeof(sa));

    while(1)
    {
        recvfrom(s,b,100,0,(struct sockaddr*)&ca,&l);
        time(&t);
        char *r=ctime(&t);
        sendto(s,r,strlen(r)+1,0,(struct sockaddr*)&ca,l);
    }
}

// This program is for the client

#include<stdio.h>
#include<string.h>
#include<arpa/inet.h>

int main()
{
    int s=socket(AF_INET,SOCK_DGRAM,0);
    struct sockaddr_in sa;
    char b[100]="TIME";

    sa.sin_family=AF_INET;
    sa.sin_port=htons(9000);
    sa.sin_addr.s_addr=inet_addr("127.0.0.1");

    sendto(s,b,strlen(b)+1,0,(struct sockaddr*)&sa,sizeof(sa));
    recvfrom(s,b,100,0,NULL,NULL);

    printf("Current Server Time: %s\n",b);
}