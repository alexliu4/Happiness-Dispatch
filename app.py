import json
import urllib
import os

from flask import Flask, escape, render_template, request, session, url_for, redirect, flash, jsonify

import random
import datetime
import time

from util import db

app = Flask(__name__)
app.secret_key = os.urandom(32)

# stubs for paths to REST APIs
WEATHER_STUB = "https://api.darksky.net/forecast/{}/{},{}" # api key, longitude, latitude
COMIC_STUB = "http://xkcd.com/info.0.json" # comic
IPAPI_STUB = "https://ipapi.co/{}/json/"
ICONS = dict()
ICONS['clear-day'] = '/static/icons/day.svg'
ICONS['clear-night'] = '/static/icons/night.svg'
ICONS['cloudy'] = '/static/icons/cloudy.svg'
ICONS['rain'] = '/static/icons/rainy-1.svg'
ICONS['snow'] = '/static/icons/snowy-1.svg'
ICONS['sleet'] = '/static/icons/rainy-7.svg'
ICONS['wind'] = '/static/icons/cloudy-day-1.svg'
ICONS['fog'] = '/static/icons/cloudy.svg'
ICONS['partly-cloudy-day'] = '/static/icons/cloudy-day-2.svg'
ICONS['partly-cloudy-night'] = '/static/icons/cloudy-night-2.svg'

def getIP():
    # use another api to get ip, returns a text
    qwerty = urllib.request.urlopen('https://api.ipify.org')
    # decode else binary
    return(qwerty.read().decode('utf-8'))

@app.route('/weather')
def weather():

    # read json file containing the api keys
    with open('data/API_Keys/keys.json') as json_file:
        json_data = json.loads(json_file.read())

    # Checking the longitude and latitiude based on the ip address
    p = urllib.request.urlopen(IPAPI_STUB.format(getIP()))
    ip = json.loads(p.read())
    location = ""
    location += ip['city'] + ", " + ip['country_name']

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        w = urllib.request.urlopen(WEATHER_STUB.format(json_data['Weather'], ip['latitude'], ip['longitude']))
    except Exception as e:
        print(e)
        return render_template('error.html', err = e)

    # Try to open up content
    try:
        f = open('data/content.json', 'r')
    except Exception as e:
        f = open('data/content.json', 'x')
    try:
        data = json.loads(f.read())
    except Exception as e:
        data = {}
    f.close()

    # if it is time to update/never had it
    # update it
    if today not in data:
        # still works with w and n defined in the try/except
        # w = urllib.request.urlopen(WEATHER_STUB.format(json_data['Weather'], ip['latitude'], ip['longitude'])) # based on your ip address location
        weather = json.loads(w.read())

        c = urllib.request.urlopen(COMIC_STUB)
        comic = json.loads(c.read())

        # Create our own json file for easier read/less space taken
        data[today] = dict()
        data[today]['weather-summary'] = weather['daily']['summary']
        data[today]['weather-hourly'] = []
        data[today]['weather-icon'] = ICONS[weather['currently']['icon']]
        # Weather hourly is a list of dictionaries containing weather info for each hour
        for hour in weather['hourly']['data']:
            d = dict()
            data[today]['weather-hourly'] += [d]
            d['time'] = hour['time']
            d['icon'] = ICONS[hour['icon']]
            temp = float(hour['temperature'])
            d['temp-f'] = str(temp).split('.')[0]
            d['temp-c'] = str((temp - 32.) * 5 / 9).split('.')[0]
            d['summary'] = hour['summary']
        data[today]['comic-image'] = comic['img']

        # Add it all to our own file
        f = open('data/content.json', 'w')
        f.write(json.dumps(data, indent=4))
        f.close()
    session['location'] = location
    session['current-hour'] = datetime.datetime.now().hour
    session['date'] = today

    need_to_warn = False
    # POPUP once per session warning of IP us
    if 'warned' not in session:
        session['warned'] = True
        need_to_warn = True
    f = float(data[today]['weather-hourly'][session['current-hour']]['temp-f'])
    c = (f - 32.) * 5 / 9
    session['temp-f'] = str(f).split('.')[0] + '°'
    session['temp-c'] = str(c).split('.')[0] + '°'
    return render_template('weather.html', background = image_of_the_day(), data = data[today], session = session, warning = need_to_warn)


def image_of_the_day():
    num_images = 8      # get 8 different images a day to use
    # uses the bing api
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0' \
            '&n={num}&mkt=en-US'.format(num=num_images)
    prefix = 'https://www.bing.com/'

    with urllib.request.urlopen(url) as f:
        result = json.loads(f.read())
    images = result['images']  # All images

    random.seed(time.time()) # to randomize the image choices
    rand_image = random.choice(images)
    image_path = rand_image['url']
    return prefix + image_path

def poem():
    url = 'https://www.poemist.com/api/v1/randompoems'
    poem = None
    while poem is None or len(poem) > 2500:
        with urllib.request.urlopen(url) as f:
            result = json.loads(f.read())
        poem = result[0]['content']
    title = result[0]['title']
    return title, poem

@app.route('/poem')
def poems():
    title,content = poem()
    return render_template(
        'poem.html',
        background = image_of_the_day(),
        title=title,
        content=content,
    )

@app.route('/comic')
def comic():
    c = urllib.request.urlopen(COMIC_STUB)
    comic = json.loads(c.read())
    return render_template(
        'comic.html',
        background = image_of_the_day(),
        comic = comic,
    )


################## OLD CODE ####################

@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'
    # return text(+12482300385)
    return render_template('login.html')


def text(to):
    from twilio.rest import Client

    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    sender = "+12626498342"
    x = 0
    while x < 3:
        x += 1
        if db.get_users_type(session['user']): # 0 is the dog but this is false
            message = client.messages.create(
                body='have a gr8 day :)',
                from_=sender,
                media_url=[catGenerator()],
                to=to
            )
            print(message.sid)
        else:
            message = client.messages.create(
                body='have a gr8 day :)',
                from_=sender,
                media_url=[dogGenerator()],
                to=to
            )
            print(message.sid)
        time.sleep(20)


def catGenerator():
    num = random.randint(0,7)
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
             "https://i.ytimg.com/vi/m2Ouo96jTFQ/hqdefault.jpg"
             ]
    return posts[num]

def dogGenerator():
    num = random.randint(0,5)
    posts = ["https://thehappypuppysite.com/wp-content/uploads/2017/10/Cute-Dog-Names-HP-long.jpg",
             "https://www.hindustantimes.com/rf/image_size_960x540/HT/p2/2018/05/16/Pictures/_1571873a-58de-11e8-b431-73159b4b09e2.jpg",
             "https://www.littlethings.com/app/uploads/2017/05/cute-dog-names-1200.jpg",
             "https://www.cheatsheet.com/wp-content/uploads/2017/10/corgi-dog-puppies.jpg",
             "http://fallinpets.com/wp-content/uploads/2017/11/dogs-cute-dog-800x445.jpg",
             # "",
             # "",
             # "",
             # "",
             # "",
             # "",
             # "",
             # "",
             # "",
             # ""
             ]
    return posts[num]

@app.route('/home')
def home():
    return render_template('home.html', background = image_of_the_day())

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

@app.route('/text')
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html', )

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
            if (r_num == db.get_users_num(r_username)):
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
    return render_template('login.html', )


@app.route('/type', methods = ["GET", "POST"])
def type():
    # print(session['user'])
    if 'user' in session:
        if 'profile' in request.args:
            name = request.args['profile'] # finds the option chosen
            # print(name)
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
