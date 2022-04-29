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
#include "stdbool.h"

#include "error/error.c"
#include "api/api.c"

int main(int argc, char *argv[]) {

    while (true) {
        int res = execute(argc, argv);
        if (res != 1) {
            error("![Panic] Ping failed");

            break;
        }

        sleep(2000);
    }

    return 0;
}