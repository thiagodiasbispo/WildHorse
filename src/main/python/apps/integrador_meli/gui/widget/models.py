from itertools import count
from typing import Iterable

from PyQt6.QtGui import QStandardItemModel, QStandardItem

from apps.integrador_meli.models import AssociacaoAtributosAutomovel

"""
    Referência: https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
"""

class AssociacaoAtributosAutomovelModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        self._data = []
        self._insert_columns()

    def get_data(self) -> Iterable[AssociacaoAtributosAutomovel]:
        return self._data

    def clear(self):
        self._data.clear()

    def _insert_columns(self):
        i = count(0)
        self.setHorizontalHeaderItem(next(i), QStandardItem("Marca"))
        self.setHorizontalHeaderItem(next(i), QStandardItem("Marca ID"))
        self.setHorizontalHeaderItem(next(i), QStandardItem("Modelo "))
        self.setHorizontalHeaderItem(next(i), QStandardItem("Modelo ID"))
        self.setHorizontalHeaderItem(next(i), QStandardItem("Ano"))
        self.setHorizontalHeaderItem(next(i), QStandardItem("Ano ID"))


    def rowCount(self, parent = ...):
        return len(self._data)

    def _set_item(self, column_index, value):
        self.setItem(self.rowCount(), column_index, QStandardItem(str(value)))

    def add_itens(self, associacoes: Iterable[AssociacaoAtributosAutomovel]):
        for associacao in associacoes:
            column_index = count()
            self._set_item(next(column_index), associacao.marca)
            self._set_item(next(column_index), associacao.marca_id)
            self._set_item(next(column_index), associacao.modelo)
            self._set_item(next(column_index), associacao.modelo_id)
            self._set_item(next(column_index), associacao.ano)
            self._set_item(next(column_index), associacao.ano_id)
            self._data.append(associacao)
