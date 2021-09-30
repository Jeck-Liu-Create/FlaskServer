# -*- encoding: utf-8 -*-
'''
@File    :   server.py    
@Contact :  tclyldx@163.com
@License :   (C)Copyright LiuDongxing,All Rights Reserved. 
             Unauthorized copying of this file, via any medium is strictly prohibited 
             Proprietary and confidential
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/9/30 13:33   LiuDongxing      1.0         None
'''

# import lib
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from main import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)  #flask默认的端口
print('run...')
IOLoop.current().start()