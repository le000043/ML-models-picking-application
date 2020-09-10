#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PREAD 0                 // index of read end of pipe
#define PWRITE 1                // index of write end of pipe
struct arg_struct {
    char *interpreter_name;
    char *python_file_name;
    char *csv_file_name;
    char *dataset_name;
    int index;
};
char *sanitize(char *);