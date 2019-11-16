# coding: utf-8
import cgi
import webapp2
import MySQLdb
import password
import json
import random
import cgi
import cgitb

def recordsession(randomid):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (id) VALUES (%s);", (randomid,))
    cursor.close()
    conn.commit()
    conn.close()

def verify_user(randomid):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM sessions WHERE id=%s;", (randomid,))
    user = cursor.fetchall()
    if len(user) != 0:
        username = user[0][0]
    else:
        username = None
    cursor.close()
    conn.commit()
    conn.close()

def formfornewusername(self):
    self.response.write("""<html>
 <head>
   <title>USER NAME SUBMISSION</title>
 </head>
 <body>
   <form method="put" action="https://ferandre14lab7.appspot.com/">
          <input type="text" name="username" Submit your Username:><br/>
          <input type="submit">
        </form>
 </body>
</html>""")
    # username=self.request.get("username")
     #return username


def updatedatabase(newusername,cookieResult):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()

    cursor.execute("UPDATE sessions SET username = %s WHERE id = %s;", (newusername,cookieResult))
    cursor.close()
    conn.commit()
    conn.close()

def checkfornulluser(cookieResult):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM sessions WHERE username is not NULL AND id=%s",(cookieResult,))
    user = cursor.fetchall()
    if len(user) != 0:
        username = user[0][0]
    else:
        username = None
    cursor.close()
    conn.commit()
    conn.close()
    return username

def verifyform():
    form = cgi.FieldStorage()
    if "name" in form:
        return form.getvalue("name")
    else:
        return None


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        cookieResult = self.request.cookies.get("firstCookie")
        #Cookie doesnt exist
        if cookieResult == None:
            #Generates random session id
            randomid = "%032x" % random.getrandbits(128)
            #set_cookie
            self.response.set_cookie("firstCookie",randomid, max_age=300)
            #inserts in database
            recordsession(randomid)
            cookieResult=randomid
            self.response.set_cookie('lastvisit', 'test', max_age=30, path='/')
            formfornewusername(self)

        if checkfornulluser(cookieResult)== None:
            formfornewusername(self)

        #username = verify_user(cookieResult)
        #checkform = verifyform()
        #if username == None and checkform != None:
            #updatedatabase(checkform,cookieResult)
        else:
            print("you are dumb")
                #check user values
                #increment_values(self)

                #Now Present form
                 #1) Take in user name
                 #2) When username is present in form update them with cookie
                #3): output the update cookie + pass username as cgo variable:
                    #self.response.write('<br>Check <a href="https:....somethingsomehingappspot.com/">value</a>')
app = webapp2.WSGIApplication([
    ("/", MainPage),
    #("/add_user", Add_User)
], debug=True)