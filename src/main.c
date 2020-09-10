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



  #define NUM  8 // including the pre-processing python script
  #define PYTHON_ARGUMENTS_SIZE 5
  #define INTERPRETER "python3"
  pthread_mutex_t mutexes[NUM];

int main(int argc, char *argv[]){
  char *csv_file_name = argv[1]; //Breast_cancer_data.csv
  // COMING UPDATE: csv_file_name will be the input from a python interface script

  //Real_estate_valuation_data_set.csv
  char *dataset_name = "";
  
  remove("output.txt");
  pthread_t *ptr = (pthread_t*)malloc(sizeof(pthread_t) * NUM);
  // creating mutex 1D array
  for (int i=0; i<NUM;i++){
    pthread_mutex_init(&mutexes[i],NULL);
  }

	void *ptr_func();

  float accuracy_array[NUM];
  // preparing algorithms array
  struct arg_struct args[NUM];
  for (int i = 0; i < NUM; i++){
    args[i].index = i;
    args[i].interpreter_name = INTERPRETER;
    args[i].csv_file_name = csv_file_name;
    args[i].dataset_name = dataset_name;
    // COMING UPDATE:
  }
    args[0].python_file_name = "pre_processing.py";
    args[1].python_file_name = "kernel_svm.py";
    args[2].python_file_name = "decision_tree_classification.py";
    args[3].python_file_name = "k_nearest_neighbors.py";
    args[4].python_file_name = "naive_bayes.py";
    args[5].python_file_name = "support_vector_machine.py";
    args[6].python_file_name = "random_forest_classification.py";
    args[7].python_file_name = "logistic_regression.py";
    // COMING UPDATE: an interface will be run to modify the csv_file_name variable
    // pre-processing
    pthread_create(&ptr[0], NULL,                 // run pre-processing python file
                       ptr_func, (void *)&args[0]);
    pthread_join(ptr[0], NULL);

    // running all algorithms
    for (int i = 1; i < NUM;i++){
      pthread_create(&ptr[i], NULL,                 // run all python files
                       ptr_func, (void *)&args[i]);
    }

    for (int i = 0; i < NUM;i++){
      pthread_join(ptr[i], NULL);
    }

    for(int i=0; i<NUM;i++){
      pthread_mutex_destroy(&mutexes[i]);
    }

    int main_out_pipe[2];
    main_out_pipe[0] = -1;
    main_out_pipe[1] = -1;

    pipe(main_out_pipe);

    pid_t main_child_pid = fork();

    int main_stdout_bak = dup(STDOUT_FILENO);

    if (main_child_pid == 0){
      // CHILD CODE
      char *arg_name = "python3";
      char *arg_list[3] = {"python3","read_file.py",NULL};

      close(main_out_pipe[PREAD]);
      dup2(main_out_pipe[PWRITE], STDOUT_FILENO);
      execvp(arg_name, arg_list);
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
		// char *argvList[4] = {"python3","helloworld.py","abc",NULL};
    char *argvList[PYTHON_ARGUMENTS_SIZE] = {args->interpreter_name,args->python_file_name,args->csv_file_name,args->dataset_name,NULL};

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
                          } else { // output ready
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
