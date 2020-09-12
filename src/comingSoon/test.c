#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/select.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <signal.h>
#include <pthread.h>
#include <ctype.h>
#include <signal.h>
#include <stdint.h>
int main(int argc, char *argv[]){
  char s[12] = "hello there";
  printf("%s\n",s );
  return 0;
}
