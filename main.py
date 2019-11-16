# coding=utf-8
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

def formfornewusername(self):
    self.response.write("""<html>
 <head>
   <title>USER NAME SUBMISSION</title>
 </head>
 <body>
<p>Welcome!!
Please enter your user name!</p>
   <form method="get" action="https://ferandre14lab7.appspot.com/">
          <input type="text" name="username" Submit your Username:><br/>
          <input type="submit">
        </form>
 </body>
</html>""")

def updatedatabase(newusername,cookieResult):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET username = %s WHERE id = %s;", (newusername,cookieResult))
    cursor.close()
    conn.commit()
    conn.close()

def checkfornulluser(cookieResult,self):
    usernameform = self.request.GET.get('username') #Get username from form
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM sessions WHERE id=(%s) and username is not NULL",(cookieResult,))
    user = cursor.fetchall()
    #if len(user)== 0:
        #cursor.execute("INSERT INTO sessions (id, username) VALUES (%s,%s)",(cookieResult,usernameform))
        #return None
    #else:
        #cursor.execute("UPDATE sessions SET username=(%s) WHERE id=(%s)",(usernameform,cookieResult))
    #user = cursor.fetchall()
    if len(user) != 0:
        #cursor.execute("UPDATE sessions SET username=(%s) WHERE id=(%s)",(usernameform,cookieResult))
        user = user[0][0]
    if len(user) == 0:
        #cursor.execute("INSERT INTO sessions (id, username) VALUES (%s,%s)",(cookieResult,usernameform))
        #recordsessions(cookieResul
        #cursor.execute("UPDATE sessions SET username=(%s) WHERE id=(%s)",(usernameform,cookieResult))
        user = None
        #self.response.write("will implement increment logic here")
    cursor.close()
    conn.commit()
    conn.close()
    return user

def cookietherebutusernull(self):
    self.response.write("""<html>
    <head>
        <title>Cookie But no Username</title>
    </head>
    <body>
    <p> You have a Cookie assicociated with this sessions but no user name!
    Please enter your user name below!</p>
    <form method="get" action="https://ferandre14lab7.appspot.com/">
          <input type="text" name="username" Submit your Username:><br/>
          <input type="submit">
        </form>
        </body>
    </html>""")
#makes sure the current user is referenced in the increments table using their cookie
def ensureIncrementData(cookieResult):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cur = conn.cursor()
    cur.execute('SELECT * FROM increments WHERE id = %s ', (cookieResult,))
    result = cur.fetchall()
    cur.close()
    #means no user under that cookie id in the increments table, then add one
    if len(result) == 0:
        cur = conn.cursor()
        cur.execute("INSERT INTO increments(id, value) VALUES(%s, %s)",(cookieResult, 0))
    conn.commit()
    cur.close()
    conn.close()

#returns the value for the specific user
def getIncrementData(cookieResult):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cur = conn.cursor()
    cur.execute('SELECT value FROM increments WHERE id = %s',(cookieResult,))
    result = cur.fetchall()
    return result[0][0]#this should always be a valid value, since ensureIncrementData() has already made an entry for this cookie

#set the increment value to what is passed in for this specific cookie user
def updateInc(cookieResult, val):
    conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
    cur = conn.cursor()
    cur.execute("UPDATE increments SET value = %s WHERE id = %s", (val,cookieResult))
    conn.commit()
    cur.close()
    conn.close()

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
            cookietherebutusernull(self):
            usernameform = self.request.GET.get('username') #Get username from form
            conn = MySQLdb.connect(unix_socket=password.SQL_HOST, user=password.SQL_USER, passwd=password.SQL_PASSWD, db="lab7")
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM sessions WHERE id=(%s) and username is not NULL",(cookieResult,))
            user = cursor.fetchall()
            cursor.execute("UPDATE sessions SET username=(%s) WHERE id=(%s)",(usernameform,cookieResult))
            cursor.close()
            conn.commit()
            conn.close()


        elif cookieResult != None and checkfornulluser(cookieResult, self) != None:
            #ensuring theres a cookie in the increments table
            ensureIncrementData(cookieResult)
            #getting the increments value for this specific cookie
            form = cgi.FieldStorage()
            #if the form has incremented/submitted already and its been passed in, then update the increments table
            if ('newInc' in form):
                updateInc(cookieResult, form['newInc'].value)
            #get most recent value
            incVal = getIncrementData(cookieResult)
            #provide a form for incrementing the value
            self.response.write('''<html><head> <title> Increment Form </title> </head>
            <body><p>This is your current increment value: {0:d}</p>
            <form method="GET" action="https://ferandre14lab7.appspot.com/">
            <button type="submit">Increment Value</button>
            <input type="hidden" name="newInc", value="{1:d}"></form></body></html>'''.format(incVal, incVal+1))

        else:
            print("ALL Cases are covered, ELSE Statement here for contingency")

app = webapp2.WSGIApplication([
    ("/", MainPage),
], debug=True)
