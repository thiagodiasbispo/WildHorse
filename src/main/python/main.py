import datetime
import sys
from pathlib import Path

import qdarktheme
from fbs_runtime.application_context import is_frozen
from fbs_runtime.application_context.PyQt6 import ApplicationContext

from comum.configuracoes.configuracao_meli_service import (
    carga_inicial_se_primeira_execucao,
    TipoAmbienteDesenvolvimento,
)
from comum.widget_utils import mostrar_mensagem_erro
from wild_horse.gui.widget.main_windows import MainWindows

path = Path(__file__).parent

if not is_frozen():

    ui_paths = (
        path / "wild_horse/gui/ui",
        path / "wild_horse/configuracoes/gui/ui",
        path / "apps/integrador_meli/gui/ui",
    )

    from comum.convert_ui_to import recompile_ui_if_changed
    from comum.compile_resources_to import recompile_resource_if_changed

    recompile_resource_if_changed()

    for app_ui_path in ui_paths:
        recompile_ui_if_changed(app_ui_path)


if __name__ == "__main__":
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    if is_frozen():
        carga_inicial_se_primeira_execucao(
            appctxt, TipoAmbienteDesenvolvimento.PRODUCAO
        )
    else:
        carga_inicial_se_primeira_execucao(
            appctxt, TipoAmbienteDesenvolvimento.HOMOLOGACAO
        )
    if datetime.date.today() > datetime.date(2025, 6, 15):
        mostrar_mensagem_erro("Esta é uma versão DEMO e sua data de validade expirou em 15/06/2025. ")
        sys.exit(0)
    appctxt.app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    window = MainWindows(appctxt)
    window.show()
    exit_code = appctxt.app.exec()  # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)
