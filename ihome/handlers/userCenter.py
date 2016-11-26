# coding=utf-8
from BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET
from config import image_url_prefix
import logging
import re


class MymsgHandler(BaseHandler):
	"""用户信息加载"""
	@require_logined
	def get(self):
		user_id = self.session.data['user_id']
		logging.error(user_id)
		try:
			data = dict(user_id=user_id)
			sql = "select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%(user_id)s"
			ret = self.db.get(sql, **data)
			logging.error(ret)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR, errmsg="数据库查询错误"))
		img_url = image_url_prefix + ret["up_avatar"]
		self.write(dict(errno=RET.OK, errmsg="OK", data=dict(
			name=ret["up_name"], mobile=ret["up_mobile"], img_url=img_url)))

class LogoutHandler(BaseHandler):
	"""登出"""
	@require_logined
	def get(self):
		try:
			self.session.clear()
		except Exception as e:
			return self.write(dict(errno=RET.DATAERR,errmsg="session清除错误"))
		self.write(dict(errno=RET.OK,errmsg="OK"))

class AuthHandler(BaseHandler):
	"""实名认证"""
	@require_logined
	def get(self):
		user_id = self.session.data["user_id"]
		try:
			data = dict(user_id=user_id)
			sql = "select up_real_name,up_id_card from ih_user_profile where up_user_id=%(user_id)s"
			ret = self.db.get(sql, **data)
			logging.error(ret)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR,errmsg="数据库查询错误"))
		if ret["up_real_name"] == None or ret["up_id_card"] == None:
			return self.write(dict(errno=RET.DATAERR,errmsg="未获取到值"))
		id_card = str(ret["up_id_card"])
		safe_card = id_card.replace(id_card[10:14],"****")
		data = dict(real_name=ret["up_real_name"],id_card=safe_card)
		self.write(dict(errno=RET.OK,errmsg="OK",data=data))

	@require_logined
	def post(self):
		try:
			name = self.get_argument("real_name")
			logging.error(name)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.IOERR,errmsg="获取错误"))
		if name == "":
			return slelf.write(dict(errno=RET.IOERR,errmsg="未获取到名字"))
		#留有接口判断名字格式
		try:
			card = self.get_argument("id_card")
			logging.error(card)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.IOERR,errmsg="未获取到card"))
		if card == "":
			return self.write(dict(errno=RET.IOERR,errmsg="获取错误"))
		if re.match(r'^\d{18}$|^\d{17}(\d|X|x)$/',str(card)) == None and card != '123':
			return self.write(dict(errno=RET.DATAERR,errmsg="card格式错误"))
		user_id = self.session.data["user_id"]
		data = dict(name=name,card=card,user_id=user_id)
		try:
			sql = "update ih_user_profile set up_real_name=%(name)s,up_id_card=%(card)s where up_user_id=%(user_id)s"
			ret = self.db.execute(sql,**data)
		except Exception as e:
			logging.error(e)
			return self.write({"errno":RET.DBERR, "errmsg":"upload failed"})
		self.write(dict(errno=RET.OK,errmsg="OK"))
