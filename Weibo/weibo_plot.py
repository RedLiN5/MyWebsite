# -*- encoding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import seaborn as sns
import glob
import os
from pymongo import MongoClient


class WeiboPlot(object):

    def __init__(self, nickname=None):
        self.nickname = nickname

    def _read_data(self):
        client = MongoClient('localhost', 27017)
        db = client['weibo']
        collection_names = db.collection_names()
        if 'data/{0}_weibos'.format(self.nickname) in collection_names:
            try:
                exec('cursor = db.' + self.nickname + '_likes.find()')
                df = pd.DataFrame(list(cursor))
            except Exception as e:
                print(e)
        else:
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
        exist_files_dir = glob.glob('../interface/app/static/plots/*.png')
        exist_files = list(map(lambda x: x.split('/')[-1], exist_files_dir))
        if file_name in exist_files:
            os.remove('../interface/app/static/plots/' + file_name)

        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("white", {"font.sans-serif": ['simhei', 'Arial']})

        fig = plt.figure(figsize=(20, 9))
        ax = fig.add_subplot(111)
        sns.despine()
        ax.plot(df_count.Date,
                df_count.Count,
                'c-',
                linewidth=2.5)
        ax.set_title('Weibo Trend of {0}'.format(self.nickname),
                     fontsize=30)
        fig.savefig('../interface/app/static/plots/' + file_name,
                    bbox_inches='tight')

    def weibo_records_plot(self):
        df = self._read_data()
        file_name = 'weibo_records_{0}.png'.format(self.nickname)
        exist_files_dir = glob.glob('../interface/app/static/plots/*.png')
        exist_files = list(map(lambda x: x.split('/')[-1], exist_files_dir))
        if file_name in exist_files:
            os.remove('../interface/app/static/plots/' + file_name)

        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("white", {"font.sans-serif": ['simhei', 'Arial']})

        df_info = df.groupby(['Date']).sum()
        table = df_info.stack().reset_index()
        table.columns = ['Date', 'Subject', 'Num']
        table['Date'] = np.array(list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),
                                          table.Date)))
        table['Unit'] = np.ones(table.shape[0])
        fig = plt.figure(figsize=(20, 9), dpi=100)
        ax = fig.add_subplot(111)
        sns.set_style("white")
        g = sns.tsplot(data=table,
                       time='Date',
                       value='Num',
                       condition='Subject',
                       unit='Unit',
                       color=sns.color_palette("Set2", 3)
                       )
        xlabel_date = list(map(lambda x: x.strftime("%Y-%m-%d"),
                               table["Date"].value_counts().index.tolist()))
        g.set_xticklabels(labels=xlabel_date,
                          rotation=30)
        sns.despine()
        ax.set_title('Weibo Records of {0}'.format(self.nickname),
                     fontsize=30)
        fig.savefig('../interface/app/static/plots/' + file_name,
                    bbox_inches='tight')

    def start_weibo_plot(self):
        self.weibo_trend_plot()
        self.weibo_records_plot()