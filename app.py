import tornado.web
import tornado.ioloop
from tornado.web import HTTPError
from Handlers.uploadHandler import UploadHandler
from Handlers.downloadHandler import DownloadHandler

def make_app():
    return tornado.web.Application([
        (r"/upload", UploadHandler),
        (r"/download/(.*)", DownloadHandler)
    ],
    debug=True,
    autoreload=True,
    )

if __name__ == '__main__':
    app = make_app()
    port = 8888
    app.listen(port)
    print(f'Server is listening on localhost on port {port}')
    
    try:
        tornado.ioloop.IOLoop.current().start()
    except HTTPError as e:
        print(f"HTTP Error: {e.status_code} - {e.reason}")