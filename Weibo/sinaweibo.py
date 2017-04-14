# -*- coding: utf-8 -*-

from likes_collect import CollectLikes
from weibos_collect import CollectWeibo
from likes_plot import LikesPlot
from weibo_plot import WeiboPlot

class SinaWeibo(object):

    def __init__(self):
        pass

    def initial(self, bloger=None, max_page=None):
        self.LikesCol = CollectLikes(bloger=bloger)
        self.WeiboCol = CollectWeibo(bloger=bloger,
                                     max_page=max_page)
        self.captcha_name = self.WeiboCol.captcha_name

    def first_part(self):
        self.LikesCol.login()
        self.LikesCol.get_likes()
        self.nickname = self.LikesCol.nickname
        self.bloger_url = self.LikesCol.bloger_page

    def second_part(self, captcha=None):
        cookie = self.WeiboCol.get_cookie(captcha=captcha)
        self.WeiboCol.get_weibo(cookie=cookie,
                                bloger_page=self.bloger_url,
                                nickname=self.nickname)
        LikesPlot(nickname=self.nickname).start_likes_plot()
        WeiboPlot(nickname=self.nickname).start_weibo_plot()
