# coding: utf-8
import cgi
import webapp2
import MySQLdb
import password
import json
import random
import cgi
import cgitb

def recordsessions(randomid):
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
   <form method="get" action="https://ferandre14lab7.appspot.com/">
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
def checkfornulluser(cookieResult,self):
    usernameform = self.request.GET.get('username')
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM sessions WHERE id=%s and username is not NULL",(cookieResult,))
    user = cursor.fetchall()
    if user== None:
        #cursor.execute("INSERT INTO sessions (id, username) VALUES (%s,%s)",(cookieResult,usernameform))
        return None
    else:
        cursor.execute("UPDATE sessions SET username=(%s) WHERE id=(%s)",(usernameform,cookieResult))
        self.response.write("will implemnt increment logic here")
    cursor.close()
    conn.commit()
    conn.close()
    return user

"""def verifyform():
    form = cgi.FieldStorage()
    if "name" in form:
        return form.getvalue("name")
    else:
        return None"""
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        cookieResult = self.request.cookies.get("firstCookie")
        #Cookie doesnt exist
        if cookieResult == None:
            #Generates random sessions id
            randomid = "%032x" % random.getrandbits(128)
            #set_cookie
            self.response.set_cookie("firstCookie",randomid, max_age=300)
            #inserts in database
            recordsessions(randomid)
            cookieResult=randomid
            formfornewusername(self)
        #when user loads the website and the user field of the sessions is null
        elif cookieResult!= None and checkfornulluser(cookieResult,self)== None:
            self.response.write("""<html>
            <head>
                <title>Cookie But no Username</title>
           </head>
            <body>
            <p> You have a cookie assicociated with this sessions but no user name!
            Please enter your user name below!</p>
            <form method="put" action="https://ferandre14lab7.appspot.com/">
                  <input type="text" name="username" Submit your Username:><br/>
                  <input type="submit">
                </form>
                </body>
            </html>""")


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
], debug=True)
