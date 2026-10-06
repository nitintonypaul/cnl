// This program is for the server

#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>

int main()
{
    int s=socket(AF_INET,SOCK_DGRAM,0);
    struct sockaddr_in sa,ca;
    socklen_t l=sizeof(ca);
    char f[100],b[2048],t[256];

    sa.sin_family=AF_INET;
    sa.sin_addr.s_addr=INADDR_ANY;
    sa.sin_port=htons(9000);
    bind(s,(struct sockaddr*)&sa,sizeof(sa));

    while(1)
    {
        memset(f,0,100);
        recvfrom(s,f,100,0,(struct sockaddr*)&ca,&l);

        if(fork()==0)
        {
            FILE *fp=fopen(f,"r");
            sprintf(b,"Handled by PID : %d\n\n",getpid());

            if(!fp)
                strcat(b,"File Not Found\n");
            else
                while(fgets(t,256,fp))
                    strcat(b,t);

            sendto(s,b,strlen(b)+1,0,(struct sockaddr*)&ca,l);
            printf("%s served by PID %d\n",f,getpid());
            return 0;
        }
    }
}

// This program is for the client

#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>

int main()
{
    int s=socket(AF_INET,SOCK_DGRAM,0);
    struct sockaddr_in sa;
    char f[100],b[2048];

    sa.sin_family=AF_INET;
    sa.sin_port=htons(9000);
    sa.sin_addr.s_addr=inet_addr("127.0.0.1");

    printf("Enter File Name : ");
    scanf("%s",f);

    sendto(s,f,strlen(f)+1,0,(struct sockaddr*)&sa,sizeof(sa));
    recvfrom(s,b,2048,0,NULL,NULL);

    printf("\n%s\n",b);
}