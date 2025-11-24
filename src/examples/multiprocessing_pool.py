import math
import sys
import time
from multiprocessing import Pool, cpu_count


def cpu_task(n: int) -> tuple[int, float]:
    # Carga CPU: raíz cuadrada sobre un rango grande
    acc = sum(math.sqrt(i + n) for i in range(300_000))
    return n, acc


def main() -> None:
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)

    datos = list(range(8))

    start = time.perf_counter()
    seq = [cpu_task(x) for x in datos]
    t_seq = time.perf_counter() - start

    start = time.perf_counter()
    with Pool(processes=cpu_count()) as pool:
        par = pool.map(cpu_task, datos)
    t_par = time.perf_counter() - start

    print(f"Secuencial: {t_seq:.3f} s")
    print(f"Paralelo ({cpu_count()} procesos): {t_par:.3f} s")
    if t_par > 0:
        print(f"Speedup: x{t_seq / t_par:.2f}")

    print("Muestras (tarea -> resultado acumulado):")
    for n, valor in par[:3]:
        print(f"  tarea {n}: {valor:.2f}")


if __name__ == '__main__':
    main()
