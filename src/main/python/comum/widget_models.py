from collections import defaultdict

import pandas as pd
from PyQt6.QtGui import QStandardItemModel, QStandardItem

"""
    Referência: https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
"""


class TableDataframeModel(QStandardItemModel):
    def __init__(self, df=None):
        super().__init__()
        self._df = None
        if df is not None:
            self.set_df(df)

    def set_df(self, df: pd.DataFrame):
        self._df = df
        self._insert_columns()
        self._add_itens()

    def clear(self):
        self._df = None

    def _insert_columns(self):
        if self._df is not None:
            for i, column in enumerate(self._df.columns):
                self.setHorizontalHeaderItem(i, QStandardItem(column))

    def rowCount(self, parent=...):
        if self._df is None:
            return 0
        return len(self._df)

    def _add_itens(self):
        columns = self._df.columns
        for i, (_, row) in enumerate(self._df.iterrows()):
            for j, column in enumerate(columns):
                self.setItem(i, j, QStandardItem(str(row[column])))


class ItemModelObjectAttributeBased(QStandardItemModel):
    def __init__(self, atributos: dict[str, str], fomatador_atributo: dict = None):
        super().__init__()
        self._data = []
        self._fomatador_atributo = fomatador_atributo
        self._atributos = atributos
        self._insert_columns()

    def get_itens(self):
        colunas = tuple(self._atributos.values())
        itens = []
        for i in range(self.rowCount()):
            item = {colunas[j] : self.item(i, j).text() for j in range(len(colunas))}
            itens.append(item)
        return itens

    def get_date(self):
        return self._data

    def _insert_columns(self):
        for i, column in enumerate(self._atributos.values()):
            self.setHorizontalHeaderItem(i, QStandardItem(column))

    def clear(self):
        self._data.clear()

    def rowCount(self, parent=...):
        return len(self._data)

    def _get_valor(self, atributo, item):
        valor = getattr(item, atributo)
        if self._fomatador_atributo and atributo in self._fomatador_atributo:
            valor = self._fomatador_atributo[atributo](valor)
        return valor

    def add_itens(self, data):
        for item in data:
            for j, atributo in enumerate(self._atributos):
                valor = self._get_valor(atributo, item)
                self.setItem(self.rowCount(), j, QStandardItem(str(valor)))
            self._data.append(item)
