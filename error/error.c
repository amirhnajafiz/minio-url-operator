#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */

// error message handler
void error(const char *msg) {
    perror(msg);
    exit(-1);
}