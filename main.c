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
        error("Parameters required: <domain> <command>");
    }

    int sock_fd, bytes, sent, receive, total;
    char message[1024], response[4096];

    sprintf(message, message_fmt, argv[1], argv[2]);
    printf("Request:\n%s\n",message);

    /* create the socket */
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        error("ERROR opening socket");
    }

    return 0;
}