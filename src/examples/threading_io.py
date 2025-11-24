import threading
import time


def fake_io(name: str, delay: float, t0: float) -> None:
    start = time.perf_counter()
    print(f"{start - t0:5.2f}s [{name}] inicio E/S simulada ({delay:.1f}s)")
    time.sleep(delay)
    end = time.perf_counter()
    print(f"{end - t0:5.2f}s [{name}] fin E/S simulada")


def main() -> None:
    tareas = [
        ("conexion-db", 2.5),
        ("descarga-api", 3.0),
        ("lectura-disco", 2.0),
    ]
    print("Threading E/S: simulamos 3 tareas I/O que se solapan (total ~3s vs ~7.5s en serie)")
    print("En CPU-bound no da speedup por el GIL, pero en I/O sí porque los hilos se alternan mientras esperan.")
    hilos = []
    t0 = time.perf_counter()
    for nombre, espera in tareas:
        t = threading.Thread(target=fake_io, args=(nombre, espera, t0), daemon=True)
        t.start()
        hilos.append(t)

    for t in hilos:
        t.join()

    total = time.perf_counter() - t0
    print(f"Tiempo total con hilos: {total:.2f}s (vs. ~{sum(d for _, d in tareas):.2f}s en serie)")


if __name__ == '__main__':
    main()
