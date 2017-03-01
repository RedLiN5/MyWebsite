# -*- encoding: utf-8 -*-
import pandas as pd

class ContactPlot(object):

    def __init__(self, bloger=None, nickname=None):
        self.bloger = bloger
        self.nickname = nickname

    def _read_data(self):
        df = pd.read_table('data/{0}_likes.csv'%{self.bloger},
                           sep=',', header=0, index_col=0)
        return df

    def _elim_own(self):
        df = self._read_data()
        pos = df.Bloger != self.nickname
        df = df.loc[pos]
        return df