# -*- coding: utf-8 -*-

from weibos_collect import CollectWeibo
from likes_plot import LikesPlot
from weibo_plot import WeiboPlot

class SinaWeibo(CollectWeibo, LikesPlot, WeiboPlot):

    def __init__(self, username=None, password=None, bloger=None, max_page=None):
        CollectWeibo.__init__(self, username=username,
                              password=password,
                              max_page=max_page,
                              bloger=bloger)
        LikesPlot.__init__(self)
        WeiboPlot.__init__(self)
        self.username = username
        self.password = password

    def run(self):
        self.login()
        self.get_likes()
        self.get_weibo()
        self.start_weibo_plot()
        self.start_likes_plot()
