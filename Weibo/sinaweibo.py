# -*- coding: utf-8 -*-

from likes_collect import CollectLikes
from weibos_collect import CollectWeibo
from likes_plot import LikesPlot
from weibo_plot import WeiboPlot

class SinaWeibo(object):

    def __init__(self, bloger=None, max_page=None):
        self.LikesCol = CollectLikes(bloger=bloger)
        self.WeiboCol = CollectWeibo(bloger=bloger,
                                     max_page=max_page)

    def start(self):
        self.LikesCol.login()
        cookie = self.LikesCol.mycookie
        self.LikesCol.get_likes()
        nickname = self.LikesCol.nickname
        bloger_url = self.LikesCol.bloger_page
        self.WeiboCol.get_weibo(cookie=cookie,
                                bloger_page=bloger_url,
                                nickname=nickname)
        LikesPlot(nickname=nickname).start_likes_plot()
        WeiboPlot(nickname=nickname).start_weibo_plot()
