# -*- encoding: utf-8 -*-
import pandas as pd
from crawler import SinaWeibo
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class WeiboPlot(SinaWeibo):

    def __init__(self):
        super(WeiboPlot, self).__init__()

    def _read_data(self):
        df = pd.read_table('data/{0}_weibos.csv'%{self.bloger},
                           sep=',', header=0, index_col=0)
        return df

    def weibo_trend_plot(self):
        df = self._read_data()
        df['Count'] = pd.Series(np.ones(df.shape[0]),
                                index=df.index)
        df_count = df[['Date', 'Count']].groupby(['Date']).sum()
        df_count['Date'] = np.array(list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),
                                             df_count.index)))
        fig = plt.figure(figsize=(20, 9))
        ax = fig.add_subplot(111)
        ax.plot(df_count.Date,
                df_count.Count,
                'c.-')
        ax.title.set_text('Weibo Trend of {0}'%{self.bloger})
        fig.savefig('plots/weibo_trend_{0}.png'%{self.bloger},
                    bbox_inches='tight')

    def weibo_records_plot(self):
        df = self._read_data()
        df['Date'] = np.array(list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),
                                       df.index)))
        df_info = df.groupby(['Date']).sum()
        fig = plt.figure(figsize=(20, 9))
        ax = fig.add_subplot(111)
        ax.plot(df_info.index,
                df_info.Like,
                'c.-')
        ax.plot(df_info.index,
                df_info.Comment,
                'g.-')
        ax.plot(df_info.index,
                df_info.Repost,
                'm.-')
        ax.title.set_text('Weibo Records of {0}' % {self.bloger})
        fig.savefig('plots/weibo_records_{0}.png' % {self.bloger},
                    bbox_inches='tight')