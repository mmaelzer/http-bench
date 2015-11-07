import tornado.ioloop
import tornado.web


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/hello", HelloHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)

    print "=== server listening on 127.0.0.1:8080 ==="
    print "begin benchmark"

    tornado.ioloop.IOLoop.current().start()

