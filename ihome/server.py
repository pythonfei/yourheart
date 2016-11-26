#coding=utf-8
"""
服务器.py , main()定义的主函数，
"""
import tornado.web
import tornado.ioloop
import tornado.httpserver
import config
import torndb,redis
from tornado.options import define,options
from urls import handler
from config import settings,mysql_options,redis_options


#定义默认值
define("port",type=int,default=8000,help='the server port')
"""重写application方法"""
class Application(tornado.web.Application):
	def __init__(self,*args,**kwargs):
		super(Application,self).__init__(*args,**kwargs)
		'链接mysql数据库'
		self.db = torndb.Connection(**mysql_options)
		'链接redis数据库'
		self.redis = redis.StrictRedis(**redis_options)

#定义主函数
def main():
	"定义logging等级"
	options.logging = config.log_level
	"定义logging文件路径"
	options.log_file_prefix = config.log_file
	options.parse_command_line()
	'创建Application实例'
	app = Application(
		handler, **settings
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.bind(options.port)
	http_server.start()
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()
