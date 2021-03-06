import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import pymongo
import md5

from tornado.options import define, options
from functools import wraps

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', WelcomeHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/guest', GuestHandler),
            (r'/user', UserHandler),
            (r'/vip', VipHandler),
            (r'/admin', AdminHandler)
        ]
        conn = pymongo.MongoClient("localhost", 27017)
        self.db = conn.week7
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)

def roles(roleslist):
    def _roles(func):
        @wraps(func)
        def __roles(self, *args, **kw):
            username = self.get_current_user()
            coll = self.application.db.users
            user_item = coll.find_one({"username": username})
            if user_item["role"] in roleslist:
                func(self, *args, **kw)
            else:
                self.clear_cookie("username")
                self.redirect("/login")
        return __roles
    return _roles



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        coll = self.application.db.users
        user_doc = coll.find_one({"username": username})
        if user_doc:
            pw = md5.new(password).hexdigest()
            if pw == user_doc["password"]:
                self.set_secure_cookie("username", self.get_argument("username"))
                self.redirect("/")
            else:
                self.redirect("/login")
        else:
            self.redirect("/login")

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)

class GuestHandler(BaseHandler):
    def get(self):
        self.render('guest.html')

class UserHandler(BaseHandler):
    @roles(['admins', 'vips', 'users'])
    def get(self):
        self.render('user.html', user=self.current_user)

class VipHandler(BaseHandler):
    @roles(['admins','vips'])
    def get(self):
        self.render('vip.html', user=self.current_user)

class AdminHandler(BaseHandler):
    @roles(['admins'])
    def get(self):
        self.render('admin.html', user=self.current_user)

class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")
            self.redirect("/")
    def post(self):
        self.clear_cookie("username")
        self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login"
    }

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()