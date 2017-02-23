# -*- coding: utf-8 -*-

from weibos_collect import CollectWeibo

class SinaWeibo(CollectWeibo):

    def __init__(self, username=None, password=None, bloger=None, max_page=None):
        super(SinaWeibo, self).__init__(max_page=max_page)
        self.username = username
        self.password = password
        self.bloger = bloger

    def run(self):
        self.login(username=self.username, password=self.password)
        self.search_bloger(bloger=self.bloger)
        self.get_weibo()