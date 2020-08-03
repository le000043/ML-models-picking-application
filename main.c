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



  #define NUM  7
  #define INTERPRETER "python3"

  pthread_mutex_t mutexes[NUM]; 

int main(int argc, char *argv[]){
  remove("output.txt");
  int num = NUM;
  pthread_t *ptr = (pthread_t*)malloc(sizeof(pthread_t) * num); 
  for (int i=0; i<num;i++){
    pthread_mutex_init(&mutexes[i],NULL);
  }

	void *ptr_func();

  float accuracy_array[num];

  struct arg_struct args[num];
  for (int i = 0; i < num; i++){
    args[i].index = i;
    args[i].arg1 = INTERPRETER;
  }
    args[0].arg2 = "kernel_svm.py";
    args[1].arg2 = "decision_tree_classification.py";
    args[2].arg2 = "k_nearest_neighbors.py";
    args[3].arg2 = "naive_bayes.py";
    args[4].arg2 = "support_vector_machine.py";
    args[5].arg2 = "random_forest_classification.py";
    args[6].arg2 = "logistic_regression.py";

    for (int i = 0; i < num;i++){
      pthread_create(&ptr[i], NULL,                 // start a user thread to read input
                       ptr_func, (void *)&args[i]);
    }
    
    for (int i = 0; i < num;i++){
      pthread_join(ptr[i], NULL);
    }

    for(int i=0; i<num;i++){
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
    char *argvList[3] = {args->arg1,args->arg2,NULL};

    close(out_pipe[PREAD]);
    dup2(out_pipe[PWRITE], STDOUT_FILENO); // Redirect stdout to pipe
		execvp(args->arg1,argvList);
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


                            // accuracy_array[args->index] = 
                          }
                          
                        }

            
    }
    return NULL;
}
