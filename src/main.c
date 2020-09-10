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

#include "runningAll.h"



  #define NUM  9 // including the pre-processing python script
  #define PYTHON_ARGUMENTS_SIZE 5
  #define INTERPRETER "python3"
  pthread_mutex_t mutexes[NUM];
  char csv_file_name[1024];
int main(int argc, char *argv[]){
  // char *csv_file_name = ""; //Breast_cancer_data.csv

  //Real_estate_valuation_data_set.csv

  remove("output.txt");
  pthread_t *ptr = (pthread_t*)malloc(sizeof(pthread_t) * NUM);
  // creating mutex 1D array
  for (int i=0; i<NUM;i++){
    pthread_mutex_init(&mutexes[i],NULL);
  }

	void *ptr_func();
  void *ptr_interface();

  float accuracy_array[NUM];
  // preparing algorithms array
  struct arg_struct args[NUM];
    // specify what python scripts to run
    args[0].python_file_name = "interface/new_interface.py";
    args[1].python_file_name = "pre_processing.py";                 // can only process numerical values for the moment
    args[2].python_file_name = "kernel_svm.py";
    args[3].python_file_name = "decision_tree_classification.py";
    args[4].python_file_name = "k_nearest_neighbors.py";
    args[5].python_file_name = "naive_bayes.py";
    args[6].python_file_name = "support_vector_machine.py";
    args[7].python_file_name = "random_forest_classification.py";
    args[8].python_file_name = "logistic_regression.py";

    // running file choosing interface
    args[0].index = 0;
    args[0].interpreter_name = INTERPRETER;
    args[0].csv_file_name = "";
    pthread_create(&ptr[0], NULL,                 // run pre-processing python file
                       ptr_interface, (void *)&args[0]);
    pthread_join(ptr[0], NULL);

    for (int i = 1; i < NUM; i++){
      args[i].index = i;
      args[i].interpreter_name = INTERPRETER;
      args[i].csv_file_name = csv_file_name;
    }
    // pre-processing including splitting train and test sets
    pthread_create(&ptr[1], NULL,
                       ptr_func, (void *)&args[1]);
    pthread_join(ptr[1], NULL);

    // running all algorithms
    for (int i = 2; i < NUM;i++){
      pthread_create(&ptr[i], NULL,                 // run all python files
                       ptr_func, (void *)&args[i]);
    }

    for (int i = 0; i < NUM;i++){                   // wait for all threads to finish
      pthread_join(ptr[i], NULL);
    }

    for(int i=0; i<NUM;i++){
      pthread_mutex_destroy(&mutexes[i]);           // clean up the auxiliary array
    }

    // create pipe
    int main_out_pipe[2];
    main_out_pipe[0] = -1;
    main_out_pipe[1] = -1;

    // code below run read_file.py to find the best model for the given dataset
    // pipe initilization
    pipe(main_out_pipe);

    pid_t main_child_pid = fork();

    int main_stdout_bak = dup(STDOUT_FILENO);

    if (main_child_pid == 0){
      // CHILD CODE
      char *arg_name = "python3";
      char *arg_list[3] = {"python3","read_file.py",NULL};

      close(main_out_pipe[PREAD]);                          // child does not need to read from the pipe
      dup2(main_out_pipe[PWRITE], STDOUT_FILENO);           // override the standard output file descriptor
      execvp(arg_name, arg_list);                           // running another program
    } else {
      // PARENT CODE
      int status;
      pid_t main_finishedPID = waitpid(main_child_pid, &status, 0);
      if (WIFEXITED(status)) {
        char result[1024];
        int main_nread = read(main_out_pipe[PREAD], &result, 1024);
        write(STDOUT_FILENO,&result,main_nread);
      }

    }
        return 0;
}
void *ptr_interface(void *arg){
  int out_pipe[2];
  out_pipe[0] = -1;
  out_pipe[1] = -1;

  int stdout_bak = dup(STDOUT_FILENO);

    struct arg_struct *args = (struct arg_struct *)arg;


  pipe(out_pipe);
	pid_t child_pid = fork();
  if(child_pid < 0) {                                   // check if fork failed
                perror("Failed to fork");                     // report errors if forking failed
                exit(1);
        }
	if (child_pid == 0) { // CHILD CODE
    char *argvList[PYTHON_ARGUMENTS_SIZE] = {args->interpreter_name,args->python_file_name,NULL};
    close(out_pipe[PREAD]);
    dup2(out_pipe[PWRITE], STDOUT_FILENO); // Redirect stdout to pipe
		execvp(args->interpreter_name,argvList);
		perror("something wrong with exec\n");
	}
  else {
  //           //PARENT CODE
            int status;
            pid_t finishedPID = waitpid(child_pid, &status, 0);
  //                       //macros used to check for exit status
                        if (WIFEXITED(status)) {
                          // child finished, time to save its result
                          close(out_pipe[PWRITE]);
                          dup2(stdout_bak, STDOUT_FILENO);  // Restore stdout: redirect to backed up fd
                          int nread = read(out_pipe[PREAD], &csv_file_name, 1024);
                          if (nread == -1){
                            perror("read failed");
                            exit(1);
                          }
                          // else { // output ready
                            // char *file_name = "output.txt";
                            // int fdout = open(file_name,O_CREAT | O_RDWR | O_APPEND, S_IRUSR | S_IWUSR);
                            // write(STDOUT_FILENO,&t,1024);

                            // pthread_mutex_lock(&mutexes[args->index]);

                            // pthread_mutex_unlock(&mutexes[args->index]);
                          // }
                        }
    }
    return NULL;
}

void *ptr_func(void *arg){
  int out_pipe[2];
  out_pipe[0] = -1;
  out_pipe[1] = -1;

  int stdout_bak = dup(STDOUT_FILENO);

    struct arg_struct *args = (struct arg_struct *)arg;


  pipe(out_pipe);
	pid_t child_pid = fork();
  if(child_pid < 0) {                                   // check if fork failed
                perror("Failed to fork");                     // report errors if forking failed
                exit(1);
        }
	if (child_pid == 0) { // CHILD CODE
    char *argvList[PYTHON_ARGUMENTS_SIZE] = {args->interpreter_name,args->python_file_name,args->csv_file_name,NULL};
    close(out_pipe[PREAD]);
    dup2(out_pipe[PWRITE], STDOUT_FILENO); // Redirect stdout to pipe
		execvp(args->interpreter_name,argvList);
		perror("something wrong with exec\n");
	}
  else {
  //           //PARENT CODE
            int status;
            pid_t finishedPID = waitpid(child_pid, &status, 0);
  //                       //macros used to check for exit status
                        if (WIFEXITED(status)) {
                          char result[1024];
                          close(out_pipe[PWRITE]);
                          dup2(stdout_bak, STDOUT_FILENO);  // Restore stdout: redirect to backed up fd
                          int nread = read(out_pipe[PREAD], &result, 1024);
                          if (nread == -1){
                            perror("read failed");
                            exit(1);
                          } else { // child output ready
                            char *file_name = "output.txt";
                            int fdout = open(file_name,O_CREAT | O_RDWR | O_APPEND, S_IRUSR | S_IWUSR);
                            // write(STDOUT_FILENO,&t,1024);
                            pthread_mutex_lock(&mutexes[args->index]);
                            write(fdout,&result,nread); // MT unsafe
                            pthread_mutex_unlock(&mutexes[args->index]);
                          }
                        }
    }
    return NULL;
}
