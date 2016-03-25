from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Restaurant</title>
    <style>
      h1 { text-align: center; }
      .content, .linker { border: 1px solid #999;
                    padding: 10px 10px;
		    margin: 10px 20%%; }
    </style>
  </head>
  <body>
    <h1>Restaurant</h1>
    <div class=content>%s</div>
    <div class=linker><a href = "/restaurant/new">Create A New Restaurant</a></div>
  </body>
</html>
'''

CONTENT = '''
<p>%(name)s</p>
<p><a href = "/restaurant/%(id)d/edit">Edit</a></p>
<p><a href = "/restaurant/%(id)d/delete">Delete</a></p>
'''

HTML_WRAP_NEW = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Add New Restaurant</title>
    <style>
      h1, form { text-align: center; }
    </style>
  </head>
  <body>
    <h1>Add New Restaurant</h1>
    <form method = 'POST' enctype = 'multipart/form-data' action='/restaurant/new'>
      <div><input name = "message" type = "text"></div>
      <div><input type = "submit", value = "Create"></div>
    </form>
  </body>
</html>
'''


HTML_WRAP_EDIT = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Edit Restaurant</title>
    <style>
      h1, form { text-align: center; }
    </style>
  </head>
  <body>
    <h1>Rename Restaurant %(name)s</h1>
    <form method = 'POST' enctype = 'multipart/form-data' action='/restaurant/%(id)d/edit'>
      <div><input name = "message" type = "text"></div>
      <div><input type = "submit", value = "Rename"></div>
    </form>
  </body>
</html>
'''

HTML_WRAP_DELETE = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Delete Restaurant</title>
    <style>
      h1, form { text-align: center; }
    </style>
  </head>
  <body>
    <h1>Are you sure you want to delete Restaurant %(name)s?</h1>
    <form method = 'POST' enctype = 'multipart/form-data' action='/restaurant/%(id)d/delete'>
      <div><input type = "submit", value = "Delete"></div>
    </form>
  </body>
</html>
'''


def getSession():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session



class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = getSession()
                restaurants = session.query(Restaurant).all()
                content = ""
                for r in restaurants:
                    content += CONTENT % {'name':r.name, 'id':r.id}
                session.close()
                self.wfile.write(HTML_WRAP % content)
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(HTML_WRAP_NEW)
                return

            if self.path.endswith("/edit"):
                reId = self.path.split('/')[-2]
                session = getSession()
                res = session.query(Restaurant).filter_by(id = reId).first()
                output = ""
                output += HTML_WRAP_EDIT % {'name':res.name, 'id':res.id}
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                reId = self.path.split('/')[-2]
                session = getSession()
                res = session.query(Restaurant).filter_by(id = reId).first()
                output = ""
                output += HTML_WRAP_DELETE % {'name':res.name, 'id':res.id}
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(output)
                return
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    session = getSession()
                    new_restaurant = Restaurant(name = messagecontent[0])
                    session.add(new_restaurant)
                    session.commit()
                    session.close()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                    restaurantId = self.path.split('/')[-2]
                    session = getSession()
                    restaurant = session.query(Restaurant).filter_by(id = restaurantId).first()
                    restaurant.name = messagecontent[0]
                    session.add(restaurant)
                    session.commit()
                    session.close()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            if self.path.endswith("/delete"):
                    restaurantId = self.path.split('/')[-2]
                    session = getSession()
                    restaurant = session.query(Restaurant).filter_by(id = restaurantId).first()
                    session.delete(restaurant)
                    session.commit()
                    session.close()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

        except:
            pass

        


def main():
    try:
        port = 8000
        server_address = ('', port)
        server = HTTPServer(server_address, WebServerHandler)
        print "Tiny web Server running on: ", server.server_address
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server..."
        server.server_close()


if __name__ == '__main__':
    main()
