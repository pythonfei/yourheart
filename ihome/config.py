#coding=utf-8
import os,base64,uuid

"""
创建配置文件
"""
#当前路径
current_path = os.path.dirname(__file__)
'设置cookie_secret的值,通过uuid和base64'
salt = base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes)
settings = {
    # 'template_path' : os.path.join(current_path,"templates"),
    'static_path' : os.path.join(current_path,'static'),
    'cookie_secret' : salt,
    'xsrf_cookies' : True,
    'debug' : True
}

"设置数据库"
mysql_options = dict(
    host = "127.0.0.1",
    database = 'ihome',
    user = 'root',
    password = 'mysql'
)
"设置缓存数据库"
redis_options = dict(
    host = "127.0.0.1",
    port = 6379
)
"日志文件路径"
log_file =os.path.join(current_path,'logs/log')
log_level = "debug"

session_expires = 86400 # session数据有效期，秒

image_url_prefix = "http://oh6xk3bcw.bkt.clouddn.com/" # 七牛图片的域名