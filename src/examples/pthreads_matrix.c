#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N 200
#define NUM_THREADS 4

typedef struct {
  int tid;
  int start_row;
  int end_row;
} thread_data_t;

static double A[N][N];
static double B[N][N];
static double C_par[N][N];
static double C_seq[N][N];

static void fill_matrices(void) {
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      A[i][j] = 1.0;
      B[i][j] = 2.0;
    }
  }
}

static void multiply_sequential(void) {
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      double sum = 0.0;
      for (int k = 0; k < N; ++k) {
        sum += A[i][k] * B[k][j];
      }
      C_seq[i][j] = sum;
    }
  }
}

void *worker(void *arg) {
  thread_data_t *t = (thread_data_t *)arg;
  printf("[Hilo %d] Filas %d-%d\n", t->tid, t->start_row, t->end_row - 1);
  for (int i = t->start_row; i < t->end_row; ++i) {
    for (int j = 0; j < N; ++j) {
      double sum = 0.0;
      for (int k = 0; k < N; ++k) {
        sum += A[i][k] * B[k][j];
      }
      C_par[i][j] = sum;
    }
  }
  return NULL;
}

static double seconds_since(struct timespec start, struct timespec end) {
  return (double)(end.tv_sec - start.tv_sec) +
         (double)(end.tv_nsec - start.tv_nsec) / 1e9;
}

int main(void) {
  pthread_t threads[NUM_THREADS];
  thread_data_t td[NUM_THREADS];

  fill_matrices();

  struct timespec t0, t1, t2;
  clock_gettime(CLOCK_MONOTONIC, &t0);
  multiply_sequential();
  clock_gettime(CLOCK_MONOTONIC, &t1);

  memset(C_par, 0, sizeof(C_par));
  int rows_per_thread = N / NUM_THREADS;
  for (int i = 0; i < NUM_THREADS; ++i) {
    td[i].tid = i;
    td[i].start_row = i * rows_per_thread;
    td[i].end_row = (i == NUM_THREADS - 1) ? N : (i + 1) * rows_per_thread;
    int rc = pthread_create(&threads[i], NULL, worker, &td[i]);
    if (rc != 0) {
      fprintf(stderr, "pthread_create fallo: %d\n", rc);
      return 1;
    }
  }

  for (int i = 0; i < NUM_THREADS; ++i) {
    pthread_join(threads[i], NULL);
  }
  clock_gettime(CLOCK_MONOTONIC, &t2);

  printf("\nResumen:\n");
  printf("  Secuencial: %.3f s  (C_seq[0][0]=%.1f)\n", seconds_since(t0, t1),
         C_seq[0][0]);
  printf("  Paralelo:   %.3f s  (C_par[0][0]=%.1f)\n", seconds_since(t1, t2),
         C_par[0][0]);
  printf("  Speedup:    x%.2f (NUM_THREADS=%d)\n",
         seconds_since(t0, t1) / seconds_since(t1, t2), NUM_THREADS);

  return 0;
}
