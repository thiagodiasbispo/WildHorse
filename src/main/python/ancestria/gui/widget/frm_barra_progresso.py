from PyQt6.QtWidgets import QDialog

from ancestria.gui.ui.barra_progresso import Ui_BarraDeProgresso


class FrmBarraProgressoWindow(QDialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.ui = Ui_BarraDeProgresso()
        self.ui.setupUi(self)

    def set_mensagem(self, mensagem):
        self.ui.lblMensagem.setText(mensagem)

    def set_minimo(self, valor):
        self.ui.progressBar.setMinimum(valor)

    def set_maximo(self, valor):
        self.ui.progressBar.setMaximum(valor)


    def set_progresso(self, valor):
        self.ui.progressBar.setValue(valor)

    def value(self):
        return self.ui.progressBar.value()

    def incremento(self, valor=25):
        if self.value() + valor >= self.ui.progressBar.maximum():
            self.set_progresso(self.ui.progressBar.minimum())
            return
        self.set_progresso(self.value() + valor)
