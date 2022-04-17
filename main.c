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
#include "error/error.c"
#include "api/api.c"

int main(int argc, char *argv[]) {

    // checking the input arguments
    if (argc < 3) {
        error("![Parameters required] <domain> <command>");
    }

    // make and http call
    http_call(argv[1], argv[2]);

    return 0;
}