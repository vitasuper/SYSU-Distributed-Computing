import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

mydictionary = []

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordsHandler)]
        f = open('dict.txt', 'r')
        lines = f.readlines()
        cnt = 0
        word = ''
        definition = ''
        for line in lines:
            cnt = cnt + 1
            if cnt % 3 == 1:
                word = line.strip('\n')
            elif cnt % 3 == 2:
                definition = line.strip('\n')
                mydictionary.append((word, definition))
                word = definition = ''
        f.close()
        tornado.web.Application.__init__(self, handlers)

class WordsHandler(tornado.web.RequestHandler):
    def get(self, word):
        flag = 0
        for item in mydictionary:
            if word == item[0]:
                self.write("Word: %s | Definition: %s \n" % (item[0], item[1]))
                flag = 1
        if flag == 0:
            self.write("ERROR: No such word in the dictionary: %s \n" %(word))

    def post(self, word):
        newDefinition = self.get_argument('newDefinition')
        flag = 0
        for item in mydictionary:
            if word == item[0]:
                self.write("Word: %s | Old definition: %s | New definition: %s \n" % (item[0], item[1], newDefinition))
                mydictionary.remove(item)
                flag = 1
        if flag == 0:
            self.write("ERROR: No such word in the dictionary: %s \n" %(word))
        else:
            mydictionary.append((word, newDefinition))
            mydictionary.sort(lambda x, y: cmp(x[0],y[0]))
            f = open('dict.txt', 'w+')
            for item in mydictionary:
                f.write(item[0] + '\n' + item[1] + '\n' + '\n')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()