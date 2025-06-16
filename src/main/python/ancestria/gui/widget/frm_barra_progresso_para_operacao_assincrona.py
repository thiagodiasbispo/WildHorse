from comum.assincrono import  ExecutorAssincronaDeFuncaoGeradoraBase
from ancestria.gui.widget.frm_barra_progresso import FrmBarraProgressoWindow


class FrmBarraProgressoParaExecucaoAssincrona(FrmBarraProgressoWindow):
    def __init__(self, executor: ExecutorAssincronaDeFuncaoGeradoraBase, mensagem = None, *args, **kwargs):
        FrmBarraProgressoWindow.__init__(self, *args, **kwargs)
        self._executor = executor
        if mensagem:
            self.set_mensagem(mensagem)

    def iniciar_carregamento_assincrono(self, incremento = 1, callback_novos_dados_carregados=None):
        self.rejected.connect(
            self._executor.requestInterruption
        )

        self._executor.erro_no_carregamento.connect(
            self.close
        )

        self._executor.finished.connect(
            self.close
        )

        self._executor.carregamento_finalizado.connect(
            self.close
        )

        if callback_novos_dados_carregados:
            self._executor.novos_dados_carregados.connect(
                callback_novos_dados_carregados
            )

        self._executor.novos_dados_carregados.connect(
            lambda _: self.incremento(incremento)
        )

        self.open()
        self._executor.start()

