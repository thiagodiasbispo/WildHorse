from itertools import count
from typing import Iterable

import pandas as pd
from PyQt6.QtGui import QStandardItemModel, QStandardItem

"""
    Referência: https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
"""


class DataframeModel(QStandardItemModel):
    def __init__(self, df = None):
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
