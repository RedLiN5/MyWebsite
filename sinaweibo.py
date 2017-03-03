# -*- coding: utf-8 -*-

from weibos_collect import CollectWeibo
from contact_plot import ContactPlot
from weibo_plot import WeiboPlot

class SinaWeibo(CollectWeibo, ContactPlot, WeiboPlot):

    def __init__(self, username=None, password=None, bloger=None, max_page=None):
        CollectWeibo.__init__(self, username=username,
                              password=password,
                              max_page=max_page,
                              bloger=bloger)
        ContactPlot.__init__(self)
        WeiboPlot.__init__(self)
        self.username = username
        self.password = password

    def run(self):
        self.login()
        self.get_likes()
        self.get_weibo()
        self.start_weibo_plot()
        self.start_contact_plot()
