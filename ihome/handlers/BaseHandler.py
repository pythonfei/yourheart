# coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import json
from tornado.options import define, options
from utils.session import Session


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def initialize(self):
        pass

    def prepare(self):
        self.xsrf_token
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def write_error(self, status_code, **kwargs):
        pass
    "将方法定义成属性"
    @property
    def db(self):
        "返回db数据库"
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def get_current_user(self):
        self.session = Session(self)
        return self.session.data


class StaticFileHandler(tornado.web.StaticFileHandler):

    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token
