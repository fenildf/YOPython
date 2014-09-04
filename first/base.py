# -*- coding:utf-8 -*-
import timeit
from tornado.web import RequestHandler

__author__ = 'striveliu'


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.dbcn




    stat_time = 0.0
    def prepare(self):
        global stat_time
        stat_time = timeit.default_timer()


    def on_finish(self):
        if self.db:
            self.db.close()
        global stat_time
        response_time = 0
        response_time = (timeit.default_timer() - stat_time) % 1000
        if response_time > 0:
            print '---------------------------RT---------------------------------'
            print '-> Current url   : ', self.request.uri
            print '-> Response time : ', response_time, ' s'
            print '--------------------------------------------------------------'
