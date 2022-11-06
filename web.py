from flask import Flask,render_template,request,redirect,url_for,session
from flask_socketio import SocketIO,send
from pymongo import MongoClient 
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import ReturnDocument

import datetime

# lcd_rs        = 22  # Note this might need to be changed to 21 for older revision Pi's.
# lcd_en        = 17
# lcd_d4        = 25
# lcd_d5        = 24
# lcd_d6        = 23
# lcd_d7        = 18
# lcd_backlight = 4

app = Flask(__name__)
app.config["SECRTE"] = "secret"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

socket = SocketIO(app,cors_allowed_origins="*")
print("Connection to mongodb")

client = MongoClient("mongodb+srv://anurag:1@cluster0.fqzjmis.mongodb.net/?retryWrites=true&w=majority")

db = client["attendence"]
user = db["user"]
attendence = db["attendence"]

@app.route("/attendence")
def index():
    
    if "user" in session:
        x = datetime.datetime.now()
        date = x.strftime("%d-%m-%Y")
        user = attendence.find({"date":date})
        print(user)
        for i in user:
            print(i)
        return render_template("index.html",data=user)
    else:
        return redirect("/")


@app.route("/",methods=["GET"])
def login():
    if "user" in session:
       return redirect("/attendence")
    else:
       return render_template("login.html")

@app.route("/loginuser",methods=["POST"])
def loginuser():
    print(request.form["name"])
    userdata = user.find_one({"name":request.form["name"]})
    print(userdata.password)
    return ""



@app.route("/logout",methods=["GET"])
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/entry",methods=["POST"])
def enter():
    n = request.form["name"]
    x = datetime.datetime.now()
    date = x.strftime("%d-%m-%Y")
    time = x.strftime("%H:%M")
    check = attendence.find_one({"name":n,"date":date})
    print(check)
    presense = user.find_one({"name":n})
    print(presense)
    if not check and presense:
        data = {
            "name":n,
            "entry": time,
            "exit" : "-",
            "date" : date
            }
        attendence.insert_one(data)
    return redirect('/')

@app.route("/exit",methods=["POST"])
def exit():
    n = request.form["name"]
    x = datetime.datetime.now()
    time = x.strftime("%H:%M")    
    check = attendence.find_one({"name":n})
    if check and check["exit"] == "-":
        attendence.find_one_and_update({"name":n},{ '$set': { "exit" : time}},return_document=ReturnDocument.AFTER)
    return redirect('/')

@app.route("/add",methods=["GET"])
def add():
    return render_template("add.html")

@app.route("/holiday",methods=["GET"])
def holiday():
    if "user" in session:
        return render_template("holiday.html")
    else:
        redirect("/")

@app.route("/addmember",methods=["POST"])
def addmember():
    n = request.form["name"]
    p = request.form["password"]
    check_user = user.find_one({"name":n})
    if not check_user:
        password = generate_password_hash(p)
        data = {
            "name":n,
            "defaultedDays":0,
            "holidays":0,
            "dates":[],
            "password": password
        }
        user.insert_one(data)
        session["user"] = n
        return redirect("/attendence")
    else:
        return "user exists"

# @app.route("/allholiday",methods=["POST"])
# def allholiday():
#     date = []
#     start = request.form["start"]
#     end = request.form["end"]
#     print(start,end)
#     date.append(start)
#     date.append(end)
#     print(date)
#     return redirect("/holiday")

@socket.on("hello")
def message():
    socket.emit("got")
    print("changinh h4")

socket.run(app,debug=True)