import datetime
import sys
from pathlib import Path

import qdarktheme
from fbs_runtime.application_context import is_frozen

from comum.configuracoes.configuracao_meli_service import (
    carga_inicial_se_primeira_execucao,
    TipoAmbienteDesenvolvimento,
)

from comum.widget_utils import mostrar_mensagem_erro

path = Path(__file__).parent

if not is_frozen():

    ui_paths = (
        path / "ancestria/gui/ui",
        path / "ancestria/configuracoes/gui/ui",
        path / "apps/integrador_meli/gui/ui",
    )

    from comum.convert_ui_to import recompile_ui_if_changed
    from comum.compile_resources_to import recompile_resource_if_changed

    recompile_resource_if_changed()

    for app_ui_path in ui_paths:
        recompile_ui_if_changed(app_ui_path)


if __name__ == "__main__":
    from fbs_runtime.application_context.PyQt6 import ApplicationContext
    from ancestria.gui.widget.main_windows import MainWindows

    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    if is_frozen():
        carga_inicial_se_primeira_execucao(
            appctxt, TipoAmbienteDesenvolvimento.PRODUCAO
        )
    else:
        carga_inicial_se_primeira_execucao(
            appctxt, TipoAmbienteDesenvolvimento.HOMOLOGACAO
        )

    appctxt.app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MainWindows(appctxt)
    window.show()
    exit_code = appctxt.app.exec()  # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)
