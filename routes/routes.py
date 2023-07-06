from flask import Flask,session, flash
import flask 
import json
import re
from flask_mail import Mail,Message
import string 
import secrets
from flask_session import Session
from werkzeug.utils import redirect
from datetime import timedelta
from functools import wraps


app= Flask(
    __name__,
    static_url_path="",
    template_folder="../UI/templates/",
    static_folder = "../UI/static/",
    )

app.config.from_pyfile("config.py")
Session(app)
mail = Mail(app)
app.secret_key="duw283rgdwq"


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email_sign2' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect('/login')
    return wrap


@app.route("/signup")
def signup():
    return flask.render_template("signup.html",action="/signup_post") 
 

@app.route("/signup_post", methods = ["POST"])
def post_signup():
    name = flask.request.form["username"]
    email_sign= flask.request.form["email_signup"]
    password = flask.request.form["password"]
    otp=""
    
    signup_data={}
    signup_data["name"]=name
    signup_data["email_sign"]=email_sign
    signup_data["password"]=password
    signup_data["otp"]=otp


    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.fullmatch(regex, email_sign):
        print("Valid email")
    else:
        return flask.render_template("errorpage.html")
    if len(name or password) < 9:
        return flask.render_template("errorpage.html")
    

    with open('data.json') as user_file:
        file_contents = user_file.read()


    parsed_json = json.loads(file_contents)
 

    for i in parsed_json['user_records']:
        if (i['email_sign']==email_sign):
            return flask.render_template("errorpage.html")


    def write_json(new_data, filename='data.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["user_records"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    

    write_json(signup_data)

    return flask.render_template("login.html")


@app.route("/")
@app.route("/homepage")
@login_required
def home():
    topic = "HELLO EVERYONE" 
    return flask.render_template("homepage.html",header=topic)


@app.route("/login")
def login():
    print('Get----')
    return flask.render_template("login.html",action="/login_post")


@app.route("/login_post", methods = ["POST"])
def post_login():
    email_sign= flask.request.form["email_signup"]
    password = flask.request.form["password"]    
    with open('data.json') as user_file:
        file_contents = user_file.read()

    parsed_json = json.loads(file_contents)

    
    for i in parsed_json['user_records']:    
        if(i['email_sign']==email_sign and i['password']==password):
            session['email_sign2']=email_sign 
            session['username']=i['name']
            return flask.render_template("Welcomepage.html")
        else: 
            login_status = "False"


    if login_status =="False":  
            return flask.render_template("errorpage.html") 
    

@app.route("/forgot")
def forgot():
    return flask.render_template("forgot.html",action="/forgot_post")


@app.route("/forgot_post", methods = ["POST"])
def post_forgot():
    email_sign= flask.request.form["email_signup"]
    print (email_sign)
    session['email_sign2']=email_sign

    with open('data.json') as user_file:
        file_contents = user_file.read()

    parsed_json = json.loads(file_contents)


    for i in parsed_json['user_records']:
        if(i['email_sign']==email_sign):
            receiver=[]
            receiver.append(email_sign)
            length=8
            characters = string.ascii_letters + string.digits + string.punctuation
            otp= "".join(secrets.choice(characters) for i in range(length))
            session['username']=i['name']
            session['otp']=otp
            msg = Message(subject='Hello ! Reset Your Password', sender='sandeshpathak282@gmail.com', recipients=receiver)
            msg.body = 'Your one time password is {}.Please use the one time password within one minutes'.format(otp)
            mail.send(msg)
            return flask.render_template("returnpage.html",action="/pwdchange_post")
        else:
            flash("The email is not available in the record.Sign in",'Wrong_Email')
            pass
    return flask.render_template("signup.html")    


@app.route("/pwdchange_post", methods = ["POST"])
def post_pwdchange():
    email_sign2 = session.get('email_sign2')
    print("The session email is",email_sign2)
    otp = session.get('otp')
    print("The otp is",otp)
    otp2=flask.request.form["user_otp"]
    if otp2==otp:
        with open('data.json','r+') as file:
            data = json.load(file)

        for user in data['user_records']:
            if (user["email_sign"]==email_sign2): 
                user["otp"] = otp;   

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        return flask.render_template("Welcomepage.html")   
    else:
        flash("You Entered the wrong OTP. Please Enter your Email Again",'Wrong_OTP')
        return redirect('/forgot')


@app.route("/newpassword")
def newpassword():
    email_sign2=session.get('email_sign2')
    print("The session value is ",email_sign2)
    if email_sign2!=None:
        return flask.render_template("newpassword.html",action="/newpassword_post")
    else:
        return flask.render_template("homepage.html")

@app.route("/newpassword_post", methods = ["POST"])
def post_newpassword():
    new_password=flask.request.form["new_password"]
    confirm_new_password=flask.request.form["confirm_new_password"]
    email_sign2=session.get('email_sign2')
    
    with open('data.json','r+') as file:
        data = json.load(file)


    for user in data['user_records']:
        if (user["email_sign"]==email_sign2 and new_password==confirm_new_password): 
            user["password"] = new_password   
            user["otp"] =""

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    return flask.render_template("login.html",action="/login_post")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect('/login')

