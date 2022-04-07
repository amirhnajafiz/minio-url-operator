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

// error message handler
void error(const char *msg) {
    perror(msg);
    exit(-1);
}

int main() {
    return 0;
}