# coding=utf-8

from BaseHandler import BaseHandler
from utils.response_code import RET
import logging
from hashlib import sha1
import re
from utils.session import Session


class LoginHandler(BaseHandler):
    """"""

    def post(self):

        mobile = self.json_args.get("mobile")
        passwd = self.json_args.get("passwd")
        logging.error(mobile)
        if not all((mobile, passwd)):
            return self.write(dict(errno=RET.DATAERR, errmsg="数据输入不全"))
        if not re.match(r"^[1][34578][0-9]{9}$", mobile):
            return self.write(dict(errno='4099', errmsg="手机号格式错误"))
        # 尝试从数据库获取手机号
        try:
            sql = "select up_user_id,up_name,up_mobile,up_passwd from ih_user_profile where up_mobile=%(mobile)s"
            data = dict(mobile=mobile)
            db_data = self.db.get(sql, **data)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询失败"))
        logging.error(db_data)
        if not db_data:
            return self.write(dict(errno=RET.DATAERR, errmsg="手机号未注册"))
        # 给密码加密
        safe_passwd = sha1(passwd).hexdigest()
        if safe_passwd != db_data['up_passwd']:
            return self.write(dict(errno=RET.DATAERR, errmsg="密码错误"))
        self.sess_obj = Session(self, mobile)
        self.sess_obj.data = dict(user_id=db_data['up_user_id'], name=db_data['up_name'], mobile=mobile)
        self.sess_obj.save()
        self.write(dict(errno=RET.OK, errmsg="OK"))
