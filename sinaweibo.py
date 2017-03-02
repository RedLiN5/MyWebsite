# -*- coding: utf-8 -*-

from weibos_collect import CollectWeibo
from contact_plot import ContactPlot
from weibo_plot import WeiboPlot

class SinaWeibo(CollectWeibo, ContactPlot, WeiboPlot):

    def __init__(self, username=None, password=None, max_page=None):
        CollectWeibo.__init__(self, username=username,
                              password=password,
                              max_page=max_page)
        ContactPlot.__init__(self)
        WeiboPlot.__init__(self)
        self.username = username
        self.password = password

    def run(self):
        self.login()
        self.search_bloger(bloger=self.bloger)
        self.get_weibo()
        self.start_weibo_plot()
        self.start_contact_plot()
