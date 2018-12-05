from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import MySQLdb
from passlib.hash import sha256_crypt


 
app = Flask(__name__)
 
@app.route('/')
def home():
    # if not session.get('logged_in'):
    return render_template('login.html')
    # else:
        # return "Hello Boss!  <a href='/logout'>Logout</a>"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    custom_flash_message ="Please Enter the valid credentials"
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    c, conn = connection()
    c.execute("select email,encrypted_password from users where email=%s", (POST_USERNAME,))
    data = c.fetchone()
    if data:
       
        print POST_USERNAME, POST_PASSWORD, data[0], data[1]
        pas_check = sha256_crypt.verify(POST_PASSWORD, data[1])
		

        if POST_USERNAME == data[0] and pas_check:
            custom_flash_message = "You are successfully logged In"
            session['logged_in'] = True

  
        else:
            # error = "Wrong password"
            # flash('wrong password!')
            custom_flash_message  = "User name or password is wrong"

    session['custom_flash'] = custom_flash_message
    return redirect("/")
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['custom_flash'] = "Successfully logged out"

    return redirect("/", code=302)

def connection():
    conn = MySQLdb.connect(host="127.0.0.1", user = "root",
                           passwd = "candy345",
                           db = "sampledb")
    c = conn.cursor()

    return c, conn

@app.route('/signup')
def signup():


    return render_template('signup.html')

@app.route('/signup_params', methods=['POST'])
def signup_params():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    enc_pass = sha256_crypt.encrypt(POST_PASSWORD)

    print POST_USERNAME, POST_PASSWORD, enc_pass, "------------------->"

    if POST_USERNAME and POST_PASSWORD:
        c, conn = connection()

        try:

            sql = "INSERT INTO users (email, encrypted_password) VALUES (%s, %s)"
            val = (POST_USERNAME, enc_pass)
            c.execute(sql, val)
            conn.commit()
            session['logged_in'] = True

        except:
             print "Something else went wrong"

    session['custom_flash'] = "Successfully sign up"

        # c.execute("insert into users email,encrypted_password from users where email=%s", (POST_USERNAME,))
    return redirect("/", code=302)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)

    app.run(host='127.0.0.1', port=8000)


    # username = "raj@gmail.com"
    # password = "candy345"