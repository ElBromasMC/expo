#!/usr/bin/env bash
set -euo pipefail

# Compila y ejecuta los ejemplos de C y prepara un entorno virtual para Python.

EXAMPLES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${EXAMPLES_DIR}/bin"
VENV_DIR="${EXAMPLES_DIR}/.venv"

mkdir -p "${BIN_DIR}"

echo "==> Compilando ejemplos C (Pthreads)"
gcc -pthread "${EXAMPLES_DIR}/pthreads_matrix.c" -o "${BIN_DIR}/pthreads_matrix"

echo "==> Compilando ejemplos C (OpenMP)"
gcc -fopenmp "${EXAMPLES_DIR}/openmp_matrix.c" -o "${BIN_DIR}/openmp_matrix"

echo "==> Ejecutando Pthreads"
"${BIN_DIR}/pthreads_matrix"

echo "==> Ejecutando OpenMP"
OMP_NUM_THREADS="${OMP_NUM_THREADS:-2}" "${BIN_DIR}/openmp_matrix"

echo "==> Creando entorno virtual para Python en ${VENV_DIR}"
python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

echo "==> Instalando dependencias Python (joblib)"
python -m pip install --upgrade pip
python -m pip install joblib

echo "==> Ejecutando multiprocessing_pool.py"
python "${EXAMPLES_DIR}/multiprocessing_pool.py"

echo "==> Ejecutando threading_io.py"
python "${EXAMPLES_DIR}/threading_io.py"

echo "==> Ejecutando joblib_parallel.py"
python "${EXAMPLES_DIR}/joblib_parallel.py"

echo "Listo."
