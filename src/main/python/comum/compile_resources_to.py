import os
import subprocess
from os import path
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
PYSIDE_RCC_PATH = Path(BASE_PATH).parent.parent.parent / '.venv_pyside6/Scripts/pyside6-rcc'

def recompile_resource_if_changed():
    for qrc_name in BASE_PATH.glob("*.qrc"):

        py_name = str(qrc_name).replace(".qrc", "_rc.py")
        py_aux = str(qrc_name).replace(".qrc", "_aux_rc.py")

        if not path.exists(py_name) or path.getmtime(qrc_name) > path.getmtime(py_name):
            print("REBUILDING RESOURCE... ", qrc_name)
            comando = f"{PYSIDE_RCC_PATH} -g python -o {py_name} {qrc_name}"

            proc = subprocess.Popen(
                comando, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            stdout, stderror = proc.communicate()

            if stdout:
                print(stdout)

            if stderror:
                print(stderror)


            with open(py_name) as fin:
                with open(py_aux, "w") as fout:
                    line = next(fin)
                    while "PySide6" not in line:
                        fout.write(line)
                        line = next(fin)
                    fout.write(line.replace("PySide6", "PyQt6"))
                    for line in fin:
                        fout.write(line)

            os.remove(py_name)
            os.rename(py_aux, py_name)


if __name__ == "__main__":
    recompile_resource_if_changed()
