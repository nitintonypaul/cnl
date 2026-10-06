// This program is for the server

#include<stdio.h>
#include<string.h>
#include<arpa/inet.h>

int main()
{
    int s=socket(AF_INET,SOCK_DGRAM,0),i;
    struct sockaddr_in sa,ca;
    socklen_t l=sizeof(ca);
    char b[1024],r[1024]="",*w;
    char *d[][2]={{"tbh","to be honest"},{"ig","I guess"},{"tbf","to be fair"},
                  {"atm","at the moment"},{"irl","in real life"},{"lol","laughing out loud"},
                  {"asap","as soon as possible"},{"omg","oh my God"},{"ttyl","talk to you later"},
                  {"idk","I don't know"},{"nvm","never mind"},{"idc","I don't care"}};

    sa.sin_family=AF_INET;
    sa.sin_addr.s_addr=INADDR_ANY;
    sa.sin_port=htons(12345);
    bind(s,(struct sockaddr*)&sa,sizeof(sa));

    recvfrom(s,b,1024,0,(struct sockaddr*)&ca,&l);

    for(w=strtok(b," \n");w;w=strtok(0," \n"))
    {
        for(i=0;i<12;i++)
            if(!strcmp(w,d[i][0])){w=d[i][1];break;}
        strcat(r,w);
        strcat(r," ");
    }

    sendto(s,r,strlen(r)+1,0,(struct sockaddr*)&ca,l);
}


// This program is for the client

#include<stdio.h>
#include<string.h>
#include<arpa/inet.h>

int main()
{
    int s=socket(AF_INET,SOCK_DGRAM,0);
    struct sockaddr_in sa;
    char b[1024];

    sa.sin_family=AF_INET;
    sa.sin_port=htons(12345);
    sa.sin_addr.s_addr=inet_addr("127.0.0.1");

    printf("Enter sentence: ");
    fgets(b,1024,stdin);

    sendto(s,b,strlen(b)+1,0,(struct sockaddr*)&sa,sizeof(sa));
    recvfrom(s,b,1024,0,NULL,NULL);

    printf("Translated: %s\n",b);
}