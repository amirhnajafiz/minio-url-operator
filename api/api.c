#include <stdlib.h> /* exit, atoi, malloc, free */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include <string.h> /* memcpy, memset */
#include <unistd.h> /* read, write, close */

void http_call(char hos[], int pot, char msg[]) {
    // defining the configs of our domain
    int port = pot;
    char *host = hos;

    // server structs
    struct hostent *server;
    struct sockaddr_in serv_address;

    int sock_fd;
    uint total;
    long bytes, sent, receive;

    char* message = msg;
    char response[4096];

    sprintf(message, "%s", hos);
    printf("Request:\n%s\n",message);

    /* create the socket */
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        error("![ERROR] opening socket");
    }

    /* lookup the ip address */
    server = gethostbyname(host);
    if (server == NULL) {
        error("![ERROR] no such host");
    }

    /* fill in the structure */
    memset(&serv_address,0,sizeof(serv_address));
    serv_address.sin_family = AF_INET;
    serv_address.sin_port = htons(port);
    memcpy(&serv_address.sin_addr.s_addr,server->h_addr,server->h_length);

    /* connect the socket */
    if (connect(sock_fd, (struct sockaddr *)&serv_address, sizeof(serv_address)) < 0) {
        error("![ERROR] connecting failed");
    }

    /* send the request byte to byte */
    total = strlen(message);
    sent = 0;
    do {
        bytes = write(sock_fd,message + sent,total - sent);
        if (bytes < 0) {
            error("![ERROR] failed writing message to socket");
        }
        if (bytes == 0)
            break;
        sent += bytes;
    } while (sent < total);

    /* receive the response byte to byte */
    memset(response, 0, sizeof(response));
    total = sizeof(response) - 1;
    receive = 0;
    do {
        bytes = read(sock_fd, response + receive, total - receive);
        if (bytes < 0)
            error("![ERROR] failed reading response from socket");
        if (bytes == 0)
            break;
        receive += bytes;
    } while (receive < total);

    /*
     * if the number of received bytes is the total size of the
     * array then we have run out of space to store the response,
     * and it hasn't all arrived yet - so that's a bad thing
     */
    if (receive == total)
        error("![ERROR] failed storing complete response from socket");

    // closing socket connection
    close(sock_fd);

    // response
    printf("[response] \n%s\n", response);
}

int execute(int argc, char *argv[]) {
    int i;

    /* first where are we going to send it? */
    int port_number = atoi(argv[2]) > 0 ? atoi(argv[2]) : 80;
    char *host = strlen(argv[1]) > 0 ? argv[1] : "localhost";
    char *message;

    // checking the input arguments
    if (argc < 5) {
        error("![Parameters required] <host> <port> <method> <path> [<data> [<headers>]]");
    }

    /* How big is the message? */
    uint message_size = 0;
    if(!strcmp(argv[3], "GET"))
    {
        message_size += strlen("%s %s%s%s HTTP/1.0\r\n");        /* method         */
        message_size += strlen(argv[3]);                         /* path           */
        message_size += strlen(argv[4]);                         /* headers        */
        if(argc > 5)
            message_size += strlen(argv[5]);                     /* query string   */
        for(i = 6; i < argc; i++)                                   /* headers        */
            message_size += strlen(argv[i]) + strlen("\r\n");
        message_size += strlen("\r\n");                          /* blank line     */
    } else {
        message_size += strlen("%s %s HTTP/1.0\r\n");
        message_size += strlen(argv[3]);                         /* method         */
        message_size += strlen(argv[4]);                         /* path           */
        for(i = 6; i < argc; i++)                                   /* headers        */
            message_size += strlen(argv[i]) + strlen("\r\n");
        if(argc > 5)
            message_size += strlen("Content-Length: %d\r\n") + 10; /* content length */
        message_size += strlen("\r\n");                            /* blank line     */
        if(argc > 5)
            message_size += strlen(argv[5]);                       /* body           */
    }

    /* allocate space for the message */
    message = malloc(message_size);

    /* fill in the parameters */
    if(!strcmp(argv[3], "GET"))
    {
        if(argc > 5)
            sprintf(message,"%s %s%s%s HTTP/1.0\r\n",
                    strlen(argv[3]) > 0 ? argv[3] : "GET",               /* method         */
                    strlen(argv[4]) > 0 ? argv[4] : "/",                 /* path           */
                    strlen(argv[5]) > 0 ? "?" : "",                      /* ?              */
                    strlen(argv[5]) > 0 ? argv[5] : "");                 /* query string   */
        else
            sprintf(message,"%s %s HTTP/1.0\r\n",
                    strlen(argv[3]) > 0 ? argv[3] : "GET",               /* method         */
                    strlen(argv[4]) > 0 ? argv[4] : "/");                /* path           */
        for(i = 6; i < argc; i++)                                           /* headers        */
            strcat(message, argv[i]); strcat(message, "\r\n");
        strcat(message, "\r\n");                                            /* blank line     */
    } else {
        sprintf(message,"%s %s HTTP/1.0\r\n",
                strlen(argv[3]) > 0 ? argv[3] : "POST",                  /* method         */
                strlen(argv[4]) > 0 ? argv[4] : "/");                    /* path           */
        for(i = 6; i < argc; i++)                                           /* headers        */
            strcat(message, argv[i]); strcat(message, "\r\n");
        if(argc > 5)
            sprintf(message + strlen(message), "Content-Length: %ld\r\n", strlen(argv[5]));
        strcat(message, "\r\n");                                /* blank line     */
        if(argc > 5)
            strcat(message, argv[5]);                           /* body           */
    }

    // make and http call
    http_call(host, port_number, message);

    return 0;
}