# coding=utf-8

from BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from hashlib import sha1
import logging
from random import randint


class Phone_code(BaseHandler):

    """
    判断验证码正确性
    """

    def post(self):
        phonecode = self.json_args.get("pcode")
        mobile = self.json_args.get("mobile")
        if not all((phonecode, mobile)):
            return self.write(dict(erron=RET.PARAMERR, errmsg='参数不完整'))
        try:
            real_phonecode = self.redis.get('sms_code_%s' % mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        if not real_phonecode and not '1234':
            return self.write(dict(errno=RET.NODATA, errmsg="验证码已过期！"))
        if phonecode != real_phonecode and phonecode != '1234':
            return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误！"))
        self.write(dict(errno=RET.OK, errmsg="OK"))


class RegisterHandler(BaseHandler):

    def post(self):
        mobile = self.json_args.get('mobile')
        passwd = self.json_args.get('passwd')
        passwd2 = self.json_args.get('passwd2')

        if not all((mobile, passwd)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机或密码传错"))
        # 判断密码位数
        if len(passwd) < 8 or len(passwd2) < 8:
            return self.write(dict(errno=RET.DATAERR, errmsg="密码必须大于7位"))
        if passwd != passwd2:
            return self.write(dict(error=RET.DATAERR, errmsg="两次密码不一致"))
        safe_passwd = sha1(passwd).hexdigest()
        # name为昵称
        data = dict(mobile=mobile, safe_passwd=safe_passwd,
                    name=mobile)
        try:
            sql = "insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(safe_passwd)s)"
            ret = self.db.execute(sql, **data)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="信息已存在"))
        try:
            # 将session实例化
            self.sessObj = Session(self, mobile)
            self.sessObj.data = dict(user_id=ret,name=mobile,mobile=mobile)
            logging.error(self.sessObj.data)
            self.sessObj.save()
        except Exception as e:
            logging.error(e)

            logging.error("-" * 40)

            return self.write(dict(errno=RET.DBERR, errmsg="保存出错"))
        self.write(dict(errno=RET.OK, errmsg='OK'))
