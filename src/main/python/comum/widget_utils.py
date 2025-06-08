from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore
import abc
import os

from PyQt6.QtWidgets import QFileDialog


def escolher_diretorio(parent, titulo="Selecione um diretório",
                       directory=os.getenv("USERPROFILE")):
    return QtWidgets.QFileDialog.getExistingDirectory(parent, caption=titulo, directory=directory,
                                                      options=QtWidgets.QFileDialog.Option.ShowDirsOnly)


def escolher_arquivo(
        parent, filtro, titulo, directory=os.getenv("USERPROFILE")
):
    arquivo = QFileDialog.getOpenFileName(
        parent, titulo, filter=filtro, directory=directory
    )
    return arquivo[0]


def escolher_panilha_excel(parent, titulo="Abrir Planilha Excel",
                           directory=os.getenv("USERPROFILE")):
    return escolher_arquivo(parent, filtro="Planilhas Excel (*.xlsx *.xls)", titulo=titulo, directory=directory)

def escolher_panilha_csv(parent, titulo="Abrir Planilha Excel",
                           directory=os.getenv("USERPROFILE")):
    return escolher_arquivo(parent, filtro="Planilhas CSV (*.csv *.CSV)", titulo=titulo, directory=directory)


def mostrar_cursor_espera():
    QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor)
    )


def restaurar_cursor():
    QtWidgets.QApplication.restoreOverrideCursor()


def get_message_box_padrao(parent):
    msg_box = QtWidgets.QMessageBox(parent)
    # msg_box.setStyleSheet("color: rgb(239, 240, 231);")
    return msg_box


def mostrar_mensagem_sucesso(parent, mensagem, titulo="Sucesso!"):
    msg_box = get_message_box_padrao(parent)
    return msg_box.information(msg_box, titulo, mensagem)


def mostrar_mensagem_erro(parent, mensagem, titulo="Erro!"):
    msg_box = get_message_box_padrao(parent)
    return msg_box.critical(msg_box, titulo, mensagem)


def mostrar_mensagem_erro_usuario_nao_autenticado(parent):
    return mostrar_mensagem_erro(parent, titulo="Erro de autenticação",
                          mensagem="Você não está autenticado! Autentique-se na tela de Configurações da Mercado Livre.")


def mostrar_mensagem_warning(parent, mensagem, titulo="Aviso!"):
    msg_box = get_message_box_padrao(parent)
    return msg_box.warning(msg_box, titulo, mensagem)
