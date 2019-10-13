from flask import Flask, escape, render_template, request, session, url_for, redirect, flash, jsonify

from twilio.rest import Client

import random
import os
import time

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
    account_sid = 'AC026b3b3de192f720297096a7a35f2877'
    auth_token = '71f6b46374bc6c9b530ac339a4944044'

    client = Client(account_sid, auth_token)
    sender = "+12626498342"
    x = 0
    while x < 3:
        x += 1
        if int(db.get_users_type(session['user'])[0][0]): # 0 is the dog but this is false
            message = client.messages.create(
                body='have a gr9 day :)',
                from_=sender,
                media_url=catGenerator(),
                to=to
            )
            print(message.sid)
            print('cat')
        else:
            message = client.messages.create(
                body='have a gr9 day :)',
                from_=sender,
                media_url=dogGenerator(),
                to=to
            )
            print(message.sid)
            print('dog')
        time.sleep(20)


def catGenerator():
    num = random.randint(0,13)
    posts = ["https://d17fnq9dkz9hgj.cloudfront.net/uploads/2018/03/Russian-Blue_01.jpg",
             "https://cdn.vox-cdn.com/thumbor/-rwMBmhqgFFjfodG72q3g-A0xPM=/0x0:750x394/1200x800/filters:focal(315x137:435x257)/cdn.vox-cdn.com/uploads/chorus_image/image/60939037/GOGHex2SIW8EkuCqnT42_385891624.0.1534632092.jpg",
             "https://i.imgur.com/epMSRQH.jpg",
             "http://fenozi.com/wp-content/uploads/2017/04/cute-cats-8.jpg",
             "https://i.pinimg.com/originals/f3/bd/84/f3bd8497e15399201b634714ec5ed390.jpg",
             "https://i.imgur.com/SFECZaY.jpg",
             "https://live.staticflickr.com/3689/8989851909_9b78222fbb.jpg",
             "https://www.mythirtyspot.com/wp-content/uploads/2014/09/Screen-Shot-2014-09-18-at-10.19.29-PM-1024x712.png",
             "https://www.chinadaily.com.cn/culture/art/img/attachement/jpg/site1/20171115/f04da2db14841b75eb5836.jpg",
             "https://www.bestfunnies.com/wp-content/uploads/2015/05/TOP-30-Cute-Cats-Cute-Cat-11.jpg",
             "https://i.ytimg.com/vi/W-PBFMECvTE/maxresdefault.jpg",
             "https://www.1800flowers.com/blog/wp-content/uploads/2016/08/cute-kitten-cat-in-flowers-1.jpg",
             "https://i.ytimg.com/vi/m2Ouo96jTFQ/hqdefault.jpg",
             "https://cdn1.imggmi.com/uploads/2019/10/12/c9fd6e30cdc52de59f0209a7b4d4aa99-full.jpg",

             ]
    return posts[num]

def dogGenerator():
    num = random.randint(0,15)
    posts = ["https://thehappypuppysite.com/wp-content/uploads/2017/10/Cute-Dog-Names-HP-long.jpg",
             "https://www.hindustantimes.com/rf/image_size_960x540/HT/p2/2018/05/16/Pictures/_1571873a-58de-11e8-b431-73159b4b09e2.jpg",
             "https://www.littlethings.com/app/uploads/2017/05/cute-dog-names-1200.jpg",
             "https://www.cheatsheet.com/wp-content/uploads/2017/10/corgi-dog-puppies.jpg",
             "http://fallinpets.com/wp-content/uploads/2017/11/dogs-cute-dog-800x445.jpg",
             "http://images2.fanpop.com/image/photos/13800000/Cute-Dog-dogs-13857490-500-341.jpg",
             "https://assets.blog.slice.ca/imageserve/wp-content/uploads/2018/04/16215645/cute-dog-names-luna/x.jpg",
             "https://i1.wp.com/s4.favim.com/orig/50/boo-cute-dog-pomeranian-Favim.com-452643.jpg",
             "https://www.sheknows.com/wp-content/uploads/2018/08/75819ba4490411e3a2410ea5f30ea1ee_8_vshu0o.jpeg",
             "https://dognamesinfo.com/wp-content/uploads/2019/02/cute-dog-husky-smiling.jpg",
             "https://cdn2-www.dogtime.com/assets/uploads/gallery/30-impossibly-cute-puppies/impossibly-cute-puppy-2.jpg",
             "https://cdn.pixabay.com/photo/2016/10/31/14/55/rottweiler-1785760__340.jpg",
             "https://en.bcdn.biz/Images/2016/9/5/5214e7dd-ece5-4d40-b3e5-6e933a15af8e.jpg",
             "https://www.cheatsheet.com/wp-content/uploads/2017/10/chow-chow-puppy.jpg",
             "https://i.redd.it/lgshxkmdoeez.jpg",
             "https://cdn1.imggmi.com/uploads/2019/10/12/c9fd6e30cdc52de59f0209a7b4d4aa99-full.jpg"
             ]
    return posts[num]

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/prevention')
def prevention():
    return render_template('prevention.html')

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
            print(r_username)
            if (r_num == str(db.get_users_num(r_username)[0][0])):
                # Log them in
                session['user'] = r_username
                print(r_num)
                # return redirect(url_for("register"))
                # Allow them to rechoose their text type
                flash('''<i>Account already made. Do you wish to choose a new text type?
                <a href="http://127.0.0.1:5000/register">Yes</a>! </i>''')
        if r_num != check_num:
            flash("Numbers do not match!")
        elif r_num.count(' ') != 0:
            flash("Numbers can not contain spaces")
        elif r_num.count('-') != 0:
            flash("Numbers can not contain '-' or anything other than numbers ")
        elif not r_username.isalnum():
            flash("Username should be alphanumeric")
        else:
            session['user'] = r_username
            db.add_user(r_username, ("+1" + r_num))
            flash("Account Created")
            return redirect(url_for("home"))
    return render_template('login.html')


@app.route('/type', methods = ["GET", "POST"])
def type():
    # print(session['user'])
    if 'user' in session:
        if 'profile' in request.args:
            name = request.args['profile'] # finds the option chosen
            print(name)
            db.add_type(session['user'], name) # updates the db photo value
            return redirect(url_for('done'))
    return redirect(url_for('login'))

@app.route('/done')
def done():
    if 'user' in session:
        print (session['user'])
        text(db.get_users_num(session['user']))
        return render_template('done.html')
    return render_template('done.html')

if __name__ == "__main__":

    app.run()

