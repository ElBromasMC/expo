#include <omp.h>
#include <stdio.h>
#include <string.h>

#define N 700

static double A[N][N];
static double B[N][N];
static double C_seq[N][N];
static double C_par[N][N];

static void fill_matrices(void) {
  #pragma omp parallel for collapse(2)
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

static void multiply_parallel(void) {
  #pragma omp parallel for
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      double sum = 0.0;
      for (int k = 0; k < N; ++k) {
        sum += A[i][k] * B[k][j];
      }
      C_par[i][j] = sum;
    }
  }
}

int main(void) {
  printf("Ejemplo OpenMP: multiplicacion %dx%d (fork-join automatizado)\n", N, N);
  printf("1) Llenamos matrices en paralelo con collapse(2).\n");
  printf("2) Medimos baseline secuencial (sin directivas).\n");
  printf("3) Medimos paralelismo con #pragma omp parallel for (planificacion estatica).\n");
  printf("4) Comparamos speedup para visualizar el beneficio de paralelizar bucles regulares.\n\n");
  fill_matrices();

  printf("Multiplicacion %dx%d con OpenMP (omp_get_max_threads=%d)\n", N, N,
         omp_get_max_threads());

  double t0 = omp_get_wtime();
  multiply_sequential();
  double t1 = omp_get_wtime();

  memset(C_par, 0, sizeof(C_par));
  double t2 = omp_get_wtime();
  multiply_parallel();
  double t3 = omp_get_wtime();

  double seq = t1 - t0;
  double par = t3 - t2;
  printf("Secuencial: %.3f s (C_seq[0][0]=%.1f)\n", seq, C_seq[0][0]);
  printf("Paralelo:   %.3f s (C_par[0][0]=%.1f) hilos=%d\n", par, C_par[0][0],
         omp_get_max_threads());
  printf("Speedup:    x%.2f\n", seq / par);

  printf("Ejemplo de asignacion: hilo 0 calcula bloques iniciales del bucle for.\n");
  return 0;
}
