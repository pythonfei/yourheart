# coding=utf-8
from BaseHandler import BaseHandler
from utils.common import require_logined
from utils.image_storage import storage
from utils.response_code import RET
from config import image_url_prefix
import logging


class ProfileHandler(BaseHandler):
	"""头像验证"""
	@require_logined
	def post(self):
		user_id = self.session.data["user_id"]
		try:
			avatar = self.request.files["avatar"][0]["body"]
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
		try:
			img_name = storage(avatar)
		except Exception as e:
			logging.error(e)
			img_name = None
		if not img_name:
			return self.write({"errno": RET.THIRDERR, "errmsg": "qiniu error"})
		try:
			ret = self.db.execute(
				"update ih_user_profile set up_avatar=%s where up_user_id=%s", img_name, user_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errno": RET.DBERR, "errmsg": "upload failed"})
		img_url = image_url_prefix + img_name
		self.write({"errno": RET.OK, "errmsg": "OK", "url": img_url})

	@require_logined
	def get(self):
		user_id = self.session.data["user_id"]
		try:
			data = dict(user_id=user_id)
			sql = "select up_avatar from ih_user_profile where up_user_id=%(user_id)s"
			ret = self.db.get(sql, **data)
			logging.error(ret)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR,errmsg="数据库查询错误"))
		img_name = ret["up_avatar"]
		if img_name == None:
			img_name = ""
		img_url = image_url_prefix + img_name
		self.write({"errno": RET.OK, "errmsg": "OK", "url": img_url})


