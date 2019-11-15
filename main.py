import webapp2
import MySQLdb
import password
import json
import random

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "application/json"
        #self.response.write("Hello World!")
        #provide a unix socket file location instead of a hostname
        # looks like "/cloudsql/ferandre14lab7:us-central1:lab7ferandre14sreya"
        #which is /cloudsql/projectname:hostlocationofdb:databasename
        #the reason for this is that its no longer an address to the database, its a local socket file
        #like a TCP socket that sits locally as opposed to on the network
        conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
        cur = conn.cursor()
        cur.execute('select * from users')
        results = cur.fetchall()
        userdata = []
        for row in results:
            userdata.append({'ID':row[0], 'NAME':row[1], 'COLOR':row[2], 'ANIMAL':row[3]})
        userdata = json.dumps(userdata, indent=2)
        self.response.write(userdata)
        '''
        cookieResult = self.request.cookies.get("firstCookie")
        if cookieResult == None: #meaning theres no cookie stored on the user's computer under that name
            self.response.set_cookie("firstCookie", random.range(0, 1000000), max_age=300) #create a cookie named firstCookie, with a
            #random number and a max age of 300 seconds
            #creating a session id that is a 128 bit random number encoded as hex
            id = "%032x" % random.getrandbits(128)
        '''

app = webapp2.WSGIApplication([
    ("/", MainPage),
], debug=True)
