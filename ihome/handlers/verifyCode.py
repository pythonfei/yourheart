#coding=utf-8

import logging
"导入常量"
import constants
import json
import re,random
"utile 本地库"
from utils.captcha.captcha import captcha
from BaseHandler import BaseHandler
from libs.yuntongxun.CCP import ccp
from random import randint
from utils.response_code import RET
"验证码处理函数"

class ImageCodeHandler(BaseHandler):
    """
    过程：前端首先使用js生成一个codeid，pcodeid默认为空，然后将codeid和pcodeid都
        写到图片的src中，以参数形式返回，src='/api/imagecode?codeid="生成值"&
        pcodeid="值"';
        ImageCodeHandler获取参数，进行判断，首先判断pcodeid有没有，如果有则删除，
        如果没有则将错误放到日志中，不出理；
        获取生成的验证码，将编号，时间，文本放到redis里面，如果出现错误，则捕获异常，
        返回前段空字符，负责设置Content-Type,文件类型，返回验证码图片
    """

    """
    通过get函数获得验证码的codeid进行判断
    如果不是第一次获取验证码，则把前一个验证码从redis删除
    """
    def get(self):
        code_id = self.get_argument('codeid')
        pre_code_id = self.get_argument('pcodeid')
        "如果有pcodeid，删除再redis的缓存"
        if pre_code_id:
            "image_code 在redis储存时，增加一个前缀，容易识别"
            "尝试删除，否则捕获异常，放到日志里"
            try:
                self.redis.delete('image_code_%s'%pre_code_id)
            except Exception as e:
                logging.error(e)
        "如果没有，则获取验证码，"
        """
        name 图片验证码名称
        text 图片验证码文本
        image 图片验证码二进制数据
        """
        "captcha 二维码生成函数"
        name,text,image = captcha.generate_captcha()
        try:
            "储存时间"
            save_time = constants.IMAGE_CODE_EXPIRES_SECONDS
            "想缓存redis里面存codeid，存时间，文本"
            self.redis.setex('image_code_%s'%code_id,save_time,text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            "设置传入文件格式"
            self.set_header("Content-Type",'image/jpg')
            "将图片返回给前端"
            self.write(image)

"手机验证类"
class PhoneHandler(BaseHandler):

    def post(self):
        "获取ajax传入的数据"
        mobile = self.json_args.get("mobile")
        image_code_id = self.json_args.get("image_code_id")
        image_code_text = self.json_args.get("image_code_text")
        "参数没有获取到，或者获取不全"
        if not all((mobile, image_code_id, image_code_text)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
        "手机号输入不正确返回手机号错误"
        if not re.match(r"^[1][34578][0-9]{9}$", mobile):
            return self.write(dict(errno='4099', errmsg="手机号错误"))
        # 判断图片验证码
        try:
            "从redis查询验证码text，验证码获取，失败则返回查询错误"
            real_image_code_text = self.redis.get("image_code_%s" % image_code_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        "从数据库拿出的信息为空，则说明验证码已经再redis中过期"
        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA, errmsg="验证码已过期！"))
        "将redis中的验证码text和ajax传入的text，进去小写格式后比较,错误返回验证码错误"
        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误！"))
        "判断手机号是否已经注册"
        sql = "select up_mobile from ih_user_profile where up_mobile=%s"%mobile
        try:
            ret = self.db.get(sql)
        except Exception as e:
            logging.error(e)
        if ret:
            return self.write(dict(errno=RET.DATAEXIST,errmsg='手机号已存在'))
        # 若成功：
        # 生成随机验证码4位
        sms_code = "%04d" % random.randint(0, 9999)
        try:
            "将生成的短信验证码放到数据库，失败返回验证码生成错误"
            self.redis.setex("sms_code_%s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="生成短信验证码错误"))
        # 发送短信
        try:
            """
                sendTemplateSMS(to,datas,tempId)
                to目标手机号，datas发送数据int，时间，tempId模板编号
                发送短信，成功则将状态返回为OK，失败则返回发送失败
            """
            ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)

            # 需要判断返回值，待实现
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送失败！"))
        self.write(dict(errno=RET.OK, errmsg="OK"))
