# -*- encoding: utf-8 -*-
import pandas as pd
from crawler import SinaWeibo

class ContactPlot(SinaWeibo):

    def __init__(self):
        super(ContactPlot, self).__init__()

    def _read_data(self):
        df = pd.read_table('data/{0}_weibos.csv'%{self.bloger},
                           sep=',', header=0, index_col=0)
        return df
