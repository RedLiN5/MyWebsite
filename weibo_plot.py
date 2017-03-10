# -*- encoding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns
import glob
import os


class WeiboPlot(object):

    def __init__(self, nickname=None):
        self.nickname = nickname

    def _read_data(self):
        df = pd.read_table('data/{0}_weibos.csv'.format(self.nickname),
                           sep=',', header=0, index_col=0)
        return df

    def weibo_trend_plot(self):
        df = self._read_data()
        df['Count'] = pd.Series(np.ones(df.shape[0]),
                                index=df.index)
        df_count = df[['Date', 'Count']].groupby(['Date']).sum()
        df_count['Date'] = np.array(list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),
                                             df_count.index)))

        file_name = 'weibo_trend_{0}.png'.format(self.nickname)
        exist_files_dir = glob.glob('interface/app/static/plots/*.png')
        exist_files = list(map(lambda x: x.split('/')[-1], exist_files_dir))
        if file_name in exist_files:
            os.remove('interface/app/static/plots/' + file_name)

        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("white", {"font.sans-serif": ['simhei', 'Arial']})

        fig = plt.figure(figsize=(20, 9))
        ax = fig.add_subplot(111)
        sns.despine()
        ax.plot(df_count.Date,
                df_count.Count,
                'c.-')
        ax.title.set_text('Weibo Trend of {0}'.format(self.nickname))
        fig.savefig('interface/app/static/plots/' + file_name,
                    bbox_inches='tight')

    def weibo_records_plot(self):
        df = self._read_data()
        file_name = 'weibo_records_{0}.png'.format(self.nickname)
        exist_files_dir = glob.glob('interface/app/static/plots/*.png')
        exist_files = list(map(lambda x: x.split('/')[-1], exist_files_dir))
        if file_name in exist_files:
            os.remove('interface/app/static/plots/' + file_name)
        # df['Date'] = np.array(list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),
        #                                df.index)))
        df_info = df.groupby(['Date']).sum()
        table = df_info.stack().reset_index()
        table.columns = ['Date', 'Kind', 'Num']
        table['Date'] = np.array(list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),
                                          table.Date)))
        table['Subject'] = np.ones(table.shape[0])
        fig = plt.figure(figsize=(7, 3), dpi=100)
        plt.xticks(rotation=35)
        ax = fig.add_subplot(111)
        sns.set_style("white")
        sns.tsplot(data=table, time='Date',
                   condition='Kind', unit='Subject', value='Num')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.title.set_text('Weibo Records of {0}'.format(self.nickname))
        fig.savefig('interface/app/static/plots/' + file_name,
                    bbox_inches='tight')

    def start_weibo_plot(self):
        self.weibo_trend_plot()
        self.weibo_records_plot()