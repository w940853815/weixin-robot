# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web
from app import app,options

class Application(tornado.web.Application):
    def __init__(self, handlers=None, default_host="", transforms=None,
                 **settings):

        tornado.web.Application.__init__(self, handlers, default_host, transforms, **settings)

def main():
    settings = {
        'debug': options.debug
    }
    Application(**settings)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(options.port)
    print "Application starts on port: ", options.port
    print "Product: ", options.production
    print "Debug:",  options.debug
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
