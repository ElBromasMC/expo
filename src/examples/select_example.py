import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZIG = ROOT / "zig" / "zig"
BUILD_FILE = ROOT / "build.zig"
VENV = ROOT / ".venv"


def clear() -> None:
  os.system("cls" if os.name == "nt" else "clear")


def python_in_venv() -> Path:
  if os.name == "nt":
    candidate = VENV / "Scripts" / "python.exe"
  else:
    candidate = VENV / "bin" / "python"
  return candidate if candidate.exists() else Path(sys.executable)


def run_cmd(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> int:
  print(f"$ {' '.join(cmd)}")
  return subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=env)


def ensure_joblib(py: Path) -> None:
  try:
    subprocess.check_call([str(py), "-c", "import joblib"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  except subprocess.CalledProcessError:
    print("Falta joblib en el entorno. Instala con:")
    if os.name == "nt":
      print(f"  {py} -m pip install joblib")
    else:
      print(f"  {py} -m pip install joblib")


def run_zig_target(target: str, env: dict | None = None) -> None:
  if not ZIG.exists():
    print(f"No se encontró {ZIG}. Asegúrate de tener Zig 0.15.2 en esa ruta.")
    return
  if not BUILD_FILE.exists():
    print(f"No se encontró {BUILD_FILE}; no hay configuración de build.")
    return
  clear()
  cmd = [str(ZIG), "build", target]
  run_cmd(cmd, cwd=ROOT, env=env)


def run_python_script(script: str) -> None:
  clear()
  py = python_in_venv()
  ensure_joblib(py)
  run_cmd([str(py), str(ROOT / script)])


def run_tui(default_threads: int) -> None:
  options = {
    "1": ("Build C (pthreads)", lambda: run_zig_target("pthreads")),
    "2": ("Run C (pthreads)", lambda: run_zig_target("run-pthreads")),
    "3": ("Build C (OpenMP)", lambda: run_zig_target("openmp")),
    "4": ("Run C (OpenMP)", lambda: run_zig_target("run-openmp", env=_omp_env(default_threads))),
    "5": ("Python multiprocessing", lambda: run_python_script("multiprocessing_pool.py")),
    "6": ("Python threading (E/S)", lambda: run_python_script("threading_io.py")),
    "7": ("Python Joblib", lambda: run_python_script("joblib_parallel.py")),
    "a": ("Todos", lambda: run_all(default_threads)),
    "q": ("Salir", None),
  }

  while True:
    clear()
    print("=== Ejemplos de paralelismo ===")
    print(f"Zig: {ZIG}")
    print(f"Venv Python: {VENV}")
    print("-------------------------------")
    for key, (label, _) in options.items():
      print(f"[{key}] {label}")
    choice = input("\nSelecciona una opción: ").strip().lower()
    action = options.get(choice, (None, None))[1]
    if choice == "q":
      break
    if action is None:
      print("Opción inválida.")
      input("Enter para continuar...")
      continue
    action()
    input("\nEnter para volver al menú...")


def run_all(default_threads: int) -> None:
  run_zig_target("pthreads")
  run_zig_target("openmp")
  run_zig_target("run-pthreads")
  run_zig_target("run-openmp", env=_omp_env(default_threads))
  run_python_script("multiprocessing_pool.py")
  run_python_script("threading_io.py")
  run_python_script("joblib_parallel.py")


def _omp_env(threads: int) -> dict:
  env = os.environ.copy()
  env["OMP_NUM_THREADS"] = str(threads)
  return env


def main() -> None:
  parser = argparse.ArgumentParser(description="Selector interactivo de ejemplos de paralelismo.")
  parser.add_argument("--example", choices=["pthreads", "run-pthreads", "openmp", "run-openmp", "multiprocessing", "threading", "joblib", "all"], help="Ejecuta directamente un ejemplo sin abrir el TUI.")
  parser.add_argument("--threads", type=int, default=4, help="Hilos para OpenMP (usado por zig build).")
  args = parser.parse_args()

  if args.example:
    if args.example == "pthreads":
      run_zig_target("pthreads")
    elif args.example == "run-pthreads":
      run_zig_target("run-pthreads")
    elif args.example == "openmp":
      run_zig_target("openmp")
    elif args.example == "run-openmp":
      run_zig_target("run-openmp", env=_omp_env(args.threads))
    elif args.example == "multiprocessing":
      run_python_script("multiprocessing_pool.py")
    elif args.example == "threading":
      run_python_script("threading_io.py")
    elif args.example == "joblib":
      run_python_script("joblib_parallel.py")
    elif args.example == "all":
      run_all(args.threads)
    return

  run_tui(args.threads)


if __name__ == "__main__":
  main()
