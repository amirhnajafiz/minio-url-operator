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
    execute(argc, argv);

    return 0;
}