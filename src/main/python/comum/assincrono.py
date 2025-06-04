import traceback

from PyQt6.QtCore import QThread, pyqtSignal


class ExecutorAssincronaDeFuncaoGeradoraBase(QThread):
    novos_dados_carregados = pyqtSignal(object)
    erro_no_carregamento = pyqtSignal(str)
    carregamento_finalizado = pyqtSignal()

    def __init__(self, funcao_geradora, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._funcao_geradora = funcao_geradora


    def run(self):
       raise NotImplementedError()


class ExecutorAssincronaDeFuncaoGeradora(ExecutorAssincronaDeFuncaoGeradoraBase):
    def __init__(self, funcao_geradora, *args, **kwargs):
        super().__init__(funcao_geradora,*args, **kwargs)

    def run(self):
        try:
            for data in self._funcao_geradora():
                if self.isInterruptionRequested():
                    return
                self.novos_dados_carregados.emit(data)
            self.carregamento_finalizado.emit()
        except Exception as e:
            self.erro_no_carregamento.emit(str(e))
            traceback.print_exc()

