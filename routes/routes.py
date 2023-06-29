from flask import Flask,session
import flask 
import json
import re
from flask_mail import Mail,Message
import string 
import secrets
from flask_session import Session

app= Flask(
    __name__,
    static_url_path="",
    template_folder="../UI/templates/",
    static_folder = "../UI/static/",
    )

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "sandeshpathak282@gmail.com"
app.config['MAIL_PASSWORD'] = "lknrkhplqrdgcqhr"


mail = Mail(app)


app.secret_key="duw283rgdwq"


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
    print(signup_data)
    print("---")


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

    return flask.render_template("homepage.html")

@app.route("/")
@app.route("/homepage")
def home():
    topic = "HELLO EVERYONE" 
    return flask.render_template("homepage.html",header=topic)


@app.route("/login")
def login():
    print('Get----')
    return flask.render_template("login.html",action="/login_post")


@app.route("/login_post", methods = ["POST"])
def post_login():
    print('post----')
    email_sign= flask.request.form["email_signup"]
    password = flask.request.form["password"]
    # print("name is =",email_sign)
    # print("password is =",password)       

    with open('data.json') as user_file:
        file_contents = user_file.read()

    parsed_json = json.loads(file_contents)
    # print(parsed_json)
    
    for i in parsed_json['user_records']:

        print("here",i["name"], i["password"])
        
        if(i['email_sign']==email_sign and i['password']==password):

            print("signed_email is",i['email_sign'])
            print("signed_password is",i['password'])
            return flask.render_template("Welcomepage.html") 
        else:
            print("error signed_email is",i['email_sign'])
            print("eeror signed_password is",i['password'])
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
            length=16
            characters = string.ascii_letters + string.digits + string.punctuation
            password= "".join(secrets.choice(characters) for i in range(length))
            session['Password2']=password
            msg = Message(subject='Hello ! Reset Your Password', sender='sandeshpathak282@gmail.com', recipients=['018bscit035@sxc.edu.np'])
            msg.body = 'Your one time password is {}'.format(password)
            mail.send(msg)
            return flask.render_template("returnpage.html",action="/pwdchange_post")
        else:
            pass
    return flask.render_template("signup.html")    


@app.route("/pwdchange_post", methods = ["POST"])
def post_pwdchange():
    email_sign2 = session.get('email_sign2')
    password3 = session.get('Password2')

    with open('data.json','r+') as file:
        data = json.load(file)


    for user in data['user_records']:
        if (user["email_sign"]==email_sign2): 
            user["password"] = password3;   


    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    return flask.render_template("login.html",action="/login_post")


@app.route("/newpassword")
def newpassword():
    return flask.render_template("newpassword.html",action="/newpassword_post")

@app.route("/newpassword_post", methods = ["POST"])
def post_newpassword():
    email_sign=flask.request.form["email_signup"]
    