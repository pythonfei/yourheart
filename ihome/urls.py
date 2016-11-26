# coding=utf-8
import os
from handlers.IndexHandler import IndexHandler
from tornado.web import StaticFileHandler
from handlers.verifyCode import ImageCodeHandler, PhoneHandler
from handlers.register import Phone_code, RegisterHandler
from handlers.BaseHandler import StaticFileHandler
from handlers.login import LoginHandler
from handlers.passport import Check_login
from handlers.profile import ProfileHandler,UserNameHandler
from handlers.userCenter import MymsgHandler,LogoutHandler,AuthHandler


handler = [
    (r'/api/imagecode', ImageCodeHandler),
    (r'/api/smscode', PhoneHandler),
    (r'/api/phoneCode', Phone_code),
    (r'/api/submitdata', RegisterHandler),
    (r'/api/logindata', LoginHandler),
    (r'/api/check_login', Check_login),
    (r'/api/profile/avatar',ProfileHandler),
    (r'/api/profile/name',UserNameHandler),
    (r'/api/mymsg',MymsgHandler),
    (r'/api/logout',LogoutHandler),
    (r'/api/auth',AuthHandler),
    (r'/(.*)', StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__),'html'), default_filename='index.html'))
]
