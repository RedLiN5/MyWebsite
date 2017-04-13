# -*- encoding: utf-8 -*-
import pandas as pd
import numpy as np
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
import os
from pymongo import MongoClient
import json


class LikesPlot(object):

    def __init__(self, nickname=None):
        self.nickname = nickname

    def _read_data(self):
        client = MongoClient('localhost', 27017)
        db = client['weibo']
        collection_names = db.collection_names()
        dataset_names = glob.glob('static/data/*.csv')
        if '{0}_likes'.format(self.nickname) in collection_names:
            try:
                cursor = eval('db.' + self.nickname + '_likes.find()')
                df = pd.DataFrame(list(cursor))
                return df
            except Exception as e:
                print('Thumbs up data cannot be retrieved for the following reason:', e)
        elif any('{0}_likes'.format(self.nickname) in name for name in dataset_names):
            df = pd.read_table('static/data/{0}_likes.csv'.format(self.nickname),
                               sep=',', header=0, index_col=0)
            client = MongoClient('localhost', 27017)
            db = client['weibo']
            records = json.loads(self.df.T.to_json()).values()
            eval('db.' + self.nickname + '_likes.insert_many(records)')
            return df
        else:
            return None

    def _elim_own(self):
        df = self._read_data()
        if isinstance(df, pd.DataFrame):
            pos = df.Bloger != self.nickname
            df = df.loc[pos]
        return df

    def _sort(self):
        df = self._elim_own()
        if isinstance(df, pd.DataFrame):
            df_plot = pd.DataFrame({'bloger': list(Counter(df.Bloger).keys()),
                                    'num': list(Counter(df.Bloger).values())})
            df_plot = df_plot.sort_values(by='num',
                                          ascending=False).reset_index(drop=True)
            if df_plot.shape[0] <= 30:
                return df_plot
            else:
                return df_plot[:30]
        else:
            df_plot = None
            return df_plot

    def start_likes_plot(self):
        df_plot = self._sort()
        if isinstance(df_plot, pd.DataFrame):
            file_name = 'weibo_likes_{0}.png'.format(self.nickname)
            exist_files_dir = glob.glob('static/plots/*.png')
            exist_files = list(map(lambda x: x.split('/')[-1], exist_files_dir))
            if file_name in exist_files:
                os.remove('static/plots/' + file_name)

            upper = max(df_plot.num)
            mpl.rcParams['font.sans-serif'] = ['SimHei']
            mpl.rcParams['font.serif'] = ['SimHei']
            sns.set_style("white", {"font.sans-serif": ['simhei', 'Arial']})
            f, ax = plt.subplots(figsize=(6, 9), dpi=100)
            frame = plt.gca()
            frame.get_yaxis().set_visible(False)
            frame.get_xaxis().set_visible(False)
            ax = f.add_subplot(111)
            sns.set_color_codes("pastel")
            sns.barplot(x="num", y="bloger", data=df_plot,
                        label="博主的赞", color="b")
            ax.set_xticklabels(np.array(list(range(0, upper + 2))))
            sns.despine(top=True, right=True, left=True)
            ax.set(xlim=(0, upper+2), ylabel="",
                   xlabel="点赞总数")
            f.savefig('static/plots/' + file_name,
                      bbox_inches='tight')
        else:
            file_name = 'weibo_likes_{0}.png'.format(self.nickname)
            plt.figure()
            plt.savefig('static/plots/' + file_name,
                        bbox_inches='tight')