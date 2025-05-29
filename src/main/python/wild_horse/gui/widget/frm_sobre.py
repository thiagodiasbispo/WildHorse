from PyQt6.QtWidgets import (
    QDialog
)

from wild_horse.gui.ui.frm_sobre import Ui_dlgSobre


class FrmSobre(QDialog):
    def __init__(self, *args, **kwargs):
        super(FrmSobre, self).__init__(*args, **kwargs)
        self.ui = Ui_dlgSobre()
        self.ui.setupUi(self)


