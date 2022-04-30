#include <string.h> /* memcpy, memset */
#include <unistd.h> /* read, write, close */
#include <stdlib.h> /* exit, atoi, malloc, free */

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