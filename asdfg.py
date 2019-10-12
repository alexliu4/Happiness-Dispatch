from flask import Flask, escape, request
import random

from welcome import welcome

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

if __name__ == "__main__":
  app.run()
