# -*- encoding: utf-8 -*-
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
import os


class LikesPlot(object):

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

    def _sort(self):
        df = self._elim_own()
        df_plot = pd.DataFrame({'bloger': list(Counter(df.Bloger).keys()),
                                'num': list(Counter(df.Bloger).values())})
        df_plot = df_plot.sort_values(by='num',
                                      ascending=False).reset_index(drop=True)
        return df_plot

    def start_likes_plot(self):
        df_plot = self._sort()
        file_name = 'weibo_likes_{0}.png' % {self.bloger}
        exist_files_dir = glob.glob('interface/app/static/plots/*.png')
        exist_files = list(map(lambda x: x.split('/')[-1], exist_files_dir))
        if file_name in exist_files:
            os.remove('interface/app/static/plots/' + file_name)

        upper = max(df_plot.num)
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        mpl.rcParams['font.serif'] = ['SimHei']
        sns.set_style("darkgrid", {"font.sans-serif": ['simhei', 'Arial']})
        f, ax = plt.subplots(figsize=(6, 15))
        sns.set_color_codes("pastel")
        sns.barplot(x="num", y="bloger", data=df_plot,
                    label="博主的赞", color="b")
        ax.set(xlim=(0, upper+1), ylabel="",
               xlabel="点赞总数")
        f.savefig('interface/app/static/plots/' + file_name,
                  bbox_inches='tight')