# -*- encoding: utf-8 -*-
import pandas as pd
from crawler import SinaWeibo

class WeiboPlot(SinaWeibo):

    def __init__(self):
        super(WeiboPlot, self).__init__()

    def _read_data(self):
        df = pd.read_table('data/{0}_likes.csv'%{self.bloger},
                           sep=',', header=0, index_col=0)
        return df

    def _elim_own(self):
        df = self._read_data()
        pos = df.Bloger != self.nickname
        df = df.loc[pos]
        return df
