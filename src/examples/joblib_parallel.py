from joblib import Parallel, delayed
import math
import time


def procesar_imagen_stub(image_id: int) -> str:
    # Carga CPU artificial para ilustrar paralelismo
    _ = sum(math.sqrt(i) for i in range(5_000_000))
    return f'Imagen {image_id} lista'


def main() -> None:
    ids = list(range(12))

    print("Ejemplo Joblib: paralelizar funciones CPU-bound con backend de procesos")
    print(f"Joblib: {len(ids)} tareas con carga sqrt(5M) cada una")
    print("1) Ejecutamos secuencial para medir baseline.")
    print("2) Ejecutamos en paralelo con Parallel/processes (evita GIL).\n")

    start = time.perf_counter()
    secuencial = [procesar_imagen_stub(i) for i in ids]
    t_seq = time.perf_counter() - start

    start = time.perf_counter()
    paralelos = Parallel(
        n_jobs=-1, prefer='processes', verbose=5
    )(delayed(procesar_imagen_stub)(i) for i in ids)
    t_par = time.perf_counter() - start

    print(f"Secuencial: {t_seq:.3f} s")
    print(f"Paralelo (Joblib): {t_par:.3f} s")
    if t_par > 0:
        print(f"Speedup: x{t_seq / t_par:.2f}")

    print("Primeros resultados en paralelo:")
    for r in paralelos[:3]:
        print(f"  {r}")


if __name__ == '__main__':
    main()
