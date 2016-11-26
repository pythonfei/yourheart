# coding=utf-8
from BaseHandler import BaseHandler
from utils.response_code import RET


class Check_login(BaseHandler):

    def get(self):

        if self.get_current_user():
            self.write({"errno": RET.OK, "errmsg": "true", "data": {
                       "name": self.session.data.get('name')}})
        else:
            self.write(dict(errno=RET.SESSIONERR, errmsg="false"))
