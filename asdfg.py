from flask import Flask, escape, render_template, request, session, url_for, redirect, flash, jsonify

import random
import os

app = Flask(__name__)


@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'
    return text(+12482300385)

def welcome():
    return("Would you like an emergency kitten or and emergency pupper (or a nightmare)?")

def text(to):
    from twilio.rest import Client

    account_sid = 'ACac004e27a21155d41defa7bed260694e'
    auth_token = 'e435901c9626edefc0f93ac10c52b41e'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(body= catGenerator(),
                to=to,
                from_="+12563882762")

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
             "https://twitter.com/EmrgencyKittens/status/1179784439238402049?s=20"]
    return posts[num]

def dogGenerator():
    return

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/auth', methods = ["POST"])
def auth():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Intermediate to authenticate login by user'''
    # # # Authenticate
    username_input = request.form.get("username")
    number_input = request.form.get("number")
    all_usernames = db.get_all_users()
    if username_input in all_usernames:
        # If the hashes match
        if md5_crypt.verify(number_input, all_usernames[username_input]):
            # Log them in
            session['user'] = username_input
            return redirect(url_for("home"))
            # Allow them to rechoose their text type
            flash("Account already made. Do you wish to choose a new text type?")
        # Failed password and username match
        else:
            # next step in the process for the new user
            session['user'] = username_input
            return redirect(url_for("home"))
            flash("Account Created")
    return redirect(url_for("login"))

@app.route('/register', methods = ["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Adding users to the database'''
    if request.form.get("username") != None:
        r_username = request.form.get("username")
        r_num = request.form.get("number")
        check_num = request.form.get("check_number")

        if r_username in db.get_all_users():
            flash("Username taken")
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
            db.add_userFull(r_username, md5_crypt.encrypt(r_password), r_question, md5_crypt.encrypt(r_answer))
            return redirect(url_for("home"))
    return render_template('login.html')

@app.route('/reset', methods = ["GET", "POST"])
def reset():
    if 'user' in session:
        return redirect(url_for('home'))
    '''To reset userpassword'''
    if request.form.get("reg_username") != None:
        r_username = request.form.get("reg_username")
        r_answer = request.form.get("reg_answer")
        r_password = request.form.get("reg_password")
        check_pass = request.form.get("check_password")
        all_usernames = db.qaDict() #Returns dict {user:answer_to_question}
        if r_username not in db.get_all_users():
            flash("Username not found")
        elif r_password != check_pass:
            flash("Passwords do not match!")
        elif r_password.count(' ') != 0:
            flash("Password can not contain spaces")
        elif not r_username.isalnum():
            flash("Username should be alphanumeric")
        else:
            session['user'] = r_username
            # checks the question and answer in the db
            if r_username in all_usernames:
                # if the hashes match
                if md5_crypt.verify(r_answer, all_usernames[r_username]):
                    # changes the user password
                    db.update_pass(r_username, md5_crypt.encrypt(r_password))
                    return redirect(url_for('home'))
                else:
                    flash("Error occurred")
    return render_template('reset.html')

@app.route('/logout', methods = ['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))

@app.route('/add', methods = ['GET', 'POST'])
def adding():
    # Add to favorite here
    user = session['user']
    timeid = request.form.get("timeid") #timeid is how we reference the article. timeid = "yyyy-mm-dd,id"
    #print(timeid, "the timeid")
    added = db.add_Fav(user, timeid)
    search(timeid)
    list = db.show_Fav(user)
    message = ""
    if added:
        message = "Successfully added article to favorites"
    else:
        message = "Cannot add the same article multiple times"
    flash(message)
    return redirect(url_for('fav'))


if __name__ == "__main__":
  app.run()
