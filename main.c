/*
 * C-ping
 * author: amirhnajafiz
 * year: 2022
 * email: najafizadeh21@gmail.com
 *
 * description:
 * c-ping is a service to check our http services by sending
 * requests to our domains and then processing the response.
 *
 */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include <string.h> /* memcpy, memset */
#include <unistd.h> /* read, write, close */

#include "error/error.c"
#include "api/api.c"

int main(int argc, char *argv[]) {
    // defining the configs of our domain
    int port = 80;
    char *host = "https://www.google.com";
    char *message_fmt = "";

    // server structs
    struct hostent *server;
    struct sockaddr_in serv_address;

    // checking the input arguments
    if (argc < 3) {
        error("![Parameters required] <domain> <command>");
    }

    int sock_fd;
    uint total;
    long bytes, sent, receive;

    char message[1024], response[4096];

    sprintf(message, message_fmt, argv[1], argv[2]);
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
        error("ERROR connecting");
    }

    /* send the request byte to byte */
    total = strlen(message);
    sent = 0;
    do {
        bytes = write(sock_fd,message + sent,total - sent);
        if (bytes < 0) {
            error("ERROR writing message to socket");
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
            error("ERROR reading response from socket");
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
        error("ERROR storing complete response from socket");

    return 0;
}