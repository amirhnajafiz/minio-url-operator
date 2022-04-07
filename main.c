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
#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */

// error message handler
void error(const char *msg) {
    perror(msg);
    exit(-1);
}

int main(int argc, char *argv[]) {
    // defining the configs of our domain
    int port = 80;
    char *host = "https://www.google.com";
    char *message = "";

    struct hostent *server;
    struct sockaddr_in serv_addr;

    if (argc < 3) {
        error("Parameters required: <domain> <command>");
    }

    return 0;
}