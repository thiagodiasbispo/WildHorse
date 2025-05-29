import codecs
from os import path
from pathlib import Path

from PyQt6.uic import compileUi


def recompile_ui_if_changed(ui_path):
    ui_path = Path(ui_path).resolve()

    for ui_name in ui_path.glob("*.ui"):
        py_name = str(ui_name).replace(".ui", ".py")

        if not path.exists(py_name) or path.getmtime(ui_name) > path.getmtime(py_name):
            print("REBUILDING ... ", ui_name)
            with codecs.open(py_name, "w", encoding="utf8") as f:
                compileUi(ui_name, f)


if __name__ == "__main__":
    recompile_ui_if_changed()
