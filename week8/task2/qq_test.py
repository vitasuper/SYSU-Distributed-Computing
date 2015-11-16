import tornado.ioloop
import tornado.web
import qq_auth

from tornado import gen

class AuthHandler(tornado.web.RequestHandler, tornadocnauth.QQ.QQMixin):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument('code', None):
            user = yield self.get_authenticated_user(
                redirect_uri='MY_URI',
                client_id=self.settings['qq_api_key'],
                client_secret=self.settings['qq_api_secret'],
                code=self.get_argument('code'))
            self.render('qq.html', user=user)
        else:
            self.authorize_redirect(
                redirect_uri='MY_URI',
                client_id=self.settings['qq_api_key'],
                )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    pth = os.path.dirname(__file__)
    app = tornado.web.Application(
        handlers = [
            (r"/", AuthHandler),
        ],
        template_path = os.path.join(pth, "templates"),
        static_path = os.path.join(pth, "static"),
        qq_api_key = 'MY_QQ_API_KEY',
        qq_api_secret = 'MY_QQ_API_SECRET',
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
    