from flask import Flask, escape, render_template, request, session, url_for, redirect, flash, jsonify

from passlib.hash import md5_crypt
import random
import os

from util import db

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'
    # return text(+12482300385)
    return render_template('login.html')

def text(to):
    from twilio.rest import Client

    account_sid = 'ACac004e27a21155d41defa7bed260694e'
    auth_token = 'e435901c9626edefc0f93ac10c52b41e'
    client = Client(account_sid, auth_token)

    sender = "+12563882762"

    # arbitrary values for now
    cat = True
    dog = False

    if (cat):
        message = client.messages \
            .create(body=catGenerator(),
                    to=to,
                    from_=sender)
        print(message.sid)

    elif (dog):
        message = client.messages \
            .create(body=dogGenerator(),
                    to=to,
                    from_=sender)
        print(message.sid)


def catGenerator():
    num = random.randint(0,9)
    posts = ["https://twitter.com/EmrgencyKittens/status/1182683535372673029?s=20",
             "https://twitter.com/EmrgencyKittens/status/1182461312795893761?s=20",
             "https://twitter.com/EmrgencyKittens/status/1182098923839729664?s=20",
             "https://twitter.com/EmrgencyKittens/status/1181958751961649152?s=20",
             "https://twitter.com/EmrgencyKittens/status/1181736539128291329?s=20",
             "https://twitter.com/EmrgencyKittens/status/1181234003027922946?s=20",
             "https://twitter.com/EmrgencyKittens/status/1181011762310795266?s=20",
             "https://twitter.com/AdorabIeAnimal/status/1177211034756497409?s=20",
             "https://twitter.com/EmrgencyKittens/status/1180649375070068739?s=20",
             "https://twitter.com/EmrgencyKittens/status/1179924597472411648?s=20",
             "https://twitter.com/EmrgencyKittens/status/1179784439238402049?s=20",
             "https://twitter.com/EmrgencyKittens/status/1176885320538828800?s=20",
             "https://twitter.com/EmrgencyKittens/status/1175575944804864001?s=20",
             "https://twitter.com/EmrgencyKittens/status/1173623861943918592?s=20",
             "https://twitter.com/EmrgencyKittens/status/1169053001052557312?s=20"
             ]
    return posts[num]

def dogGenerator():
    num = random.randint(0, 19)
    posts = ["https://twitter.com/CuteEmergency/status/1182829488998158336?s=20",
             "https://twitter.com/CuteEmergency/status/1182640242664312832?s=20",
             "https://twitter.com/CuteEmergency/status/1178843222140968960?s=20",
             "https://twitter.com/CuteEmergency/status/1178480833277153281?s=20",
             "https://twitter.com/CuteEmergency/status/1177929200709328896?s=20",
             "https://twitter.com/CuteEmergency/status/1177393669705535488?s=20",
             "https://twitter.com/mindywhite/status/1177032897083125762?s=20",
             "https://twitter.com/CuteEmergency/status/1176306508025466881?s=20",
             "https://twitter.com/CuteEmergency/status/1175030094911459329?s=20",
             "https://twitter.com/CuteEmergency/status/1174856953790640129?s=20",
             "https://twitter.com/CuteEmergency/status/1174667706823565314?s=20",
             "https://twitter.com/CuteEmergency/status/1173942931234988033?s=20",
             "https://twitter.com/CuteEmergency/status/1173769792261677056?s=20",
             "https://twitter.com/CuteEmergency/status/1173218159370919936?s=20",
             "https://twitter.com/CuteEmergency/status/1172538376467206145?s=20",
             "https://twitter.com/CuteEmergency/status/1171957854787518464?s=20",
             #anna
             "https://ibb.co/VmK5z8Q",
             "https://twitter.com/CuteEmergency/status/1171043835570507776?s=20",
             "https://twitter.com/CuteEmergency/status/1170145911789559808?s=20",
             "https://twitter.com/CuteEmergency/status/1169231894774505476?s=20",
             "https://twitter.com/CuteEmergency/status/1168333978446835714?s=20",
             "https://twitter.com/CuteEmergency/status/1166061511166648322?s=20" ]
    return posts[num]

@app.route('/home')
def home():
    return render_template('home.html')

# @app.route('/auth', methods = ["POST"])
# def auth():
#     if 'user' in session:
#         return redirect(url_for('home'))
#     '''Intermediate to authenticate login by user'''
#     # # # Authenticate
#     username_input = request.form.get("username")
#     number_input = request.form.get("number")
#     all_usernames = db.get_all_users()
#     if username_input in all_usernames:
#         # If the hashes match
#         if md5_crypt.verify(number_input, all_usernames[username_input]):
#             # Log them in
#             session['user'] = username_input
#             return redirect(url_for("home"))
#             # Allow them to rechoose their text type
#             flash("Account already made. Do you wish to choose a new text type?")
#         # Failed password and username match
#         else:
#             # next step in the process for the new user
#             session['user'] = username_input
#             return redirect(url_for("home"))
#             flash("Account Created")
#     return redirect(url_for("login"))

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods = ["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Adding users to the database'''
    if request.form.get("username") != None:
        r_username = request.form.get("username")
        r_num = request.form.get("number")
        check_num = request.form.get("check_number")
        all_usernames = db.get_all_users()

        if r_username in all_usernames:
            # If the hashes match
            if md5_crypt.verify(number_input, all_usernames[username_input]):
                # Log them in
                session['user'] = username_input
                return redirect(url_for("home"))
                # Allow them to rechoose their text type
                flash("Account already made. Do you wish to choose a new text type?")
        elif r_num != check_num:
            flash("Numbers do not match!")
        elif r_num.count(' ') != 0:
            flash("Numbers can not contain spaces")
        elif r_num.count('-') != 0:
            flash("Numbers can not contain '-' or anything other than numbers ")
        elif not r_username.isalnum():
            flash("Username should be alphanumeric")
        else:
            session['user'] = r_username
            db.add_user(r_username, md5_crypt.encrypt(r_num))
            flash("Account Created")
            return redirect(url_for("home"))
    return render_template('login.html')


if __name__ == "__main__":

    def foo():
        app.run()

    x = 0
    while x < 3:
        foo()
        x += 1
        time.sleep(60)
