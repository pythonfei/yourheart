#coding=utf-8
from BaseHandler import BaseHandler

"定义indexhandler视图类"
class IndexHandler(BaseHandler):
    def get(self):
        self.write('hello world')
