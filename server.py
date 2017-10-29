from flask import Flask, render_template
from flask import session as flask_session
from flask_ask import Ask, statement, question, session, context
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

import logging
import nexmo
import json
import requests
import time
import unidecode
import datetime
import os

########################
#     Flask Set Up     #
########################

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")
app.config['SECRET_KEY'] = 'r2d2isarealg'

########################
#      SQLAlchemy      #
########################

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class AlexaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    question_value = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __str__(self):
        return str(self.question_id)

########################
#     Flask WTForms    #
########################

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

########################
#     Nexmo Set Up     #
########################

NEXMO_API_KEY = 'a55de8fb'
NEXMO_API_SECRET = 'cef801109554098a'
NEXMO_NUMBER = 12013505796

nexmo_client = nexmo.Client(
    key = NEXMO_API_KEY, secret = NEXMO_API_SECRET
)

########################
#        Routes        #
########################

@app.route('/', methods=('GET', 'POST'))
def landing():
    form = LoginForm()
    return render_template('landing.html', form=form)

@app.route('/dashboard', methods=('GET', 'POST'))
def user():
    # Get 14 most recent questions.
    recent_questionaire = AlexaData.query.order_by(AlexaData.timestamp.desc()).limit(13).all()
    # Sort these questions by question_id.
    recent_questionaire.sort(key=lambda question: question.question_id)

    return render_template('analytics.html', questionaire_points=recent_questionaire)

@app.route('/asdf', methods=('GET', 'POST'))
def asdf():
    all_questions = AlexaData.query.all()
    test = []
    for item in all_questions:
        test.append(item.timestamp)

    return str(test)

# ########################
# #  Get Alexa Location  #
# ########################
#
# def getLocation():
#     URL =  "https://api.amazonalexa.com/v1/devices/{}/settings/address".format(context.System.device.deviceId)
#     TOKEN =  context.System.user.permissions.consentToken
#     HEADER = {'Accept': 'application/json',
#              'Authorization': 'Bearer {}'.format(TOKEN)}
#     r = requests.get(URL, headers=HEADER)
#     if r.status_code == 200:
#         return(r.json())

########################
#       Send SMS       #
########################

def send_sms(msg_type):

    to_number = 13143595216
    if msg_type == 'default':
        message = 'Ryan has started the Keep Me Safe app. Please be on alert.'
    elif msg_type == 'no_response':
        message = 'Ryan is unresponsive. Please take immediate action if possible.'
    elif msg_type == 'emergency':
        message = 'Ryan is currently in the state of an emergency. We have contacted emergency services. Please take immediate action if possible.'

    result = nexmo_client.send_message({
        'from': NEXMO_NUMBER,
        'to': to_number,
        'text': message,
    })

    return 'asdf'

########################
#   Alexa Data to DB   #
########################

def alexaToDb(points_array):

    timestamp = datetime.datetime.now()

    for index, question in enumerate(points_array):
        alexaData = AlexaData(question_id=index, question_value=question, timestamp=timestamp)
        db.session.add(alexaData)
        db.session.commit()

    return

########################
#         Alexa        #
########################

@ask.launch
def start_skill():
    # Initializing session variables #
    session.attributes['question_array'] = [
        'Do you feel tense or wound up?',
        'Do you still enjoy the things you used to enjoy?',
        'Do you have a sort of frightened feeling as if something awful is about to happen?',
        'Can you laugh and see the funny side of things?',
        'Are worrying thoughts running through your mind?',
        'Do you feel cheerful?',
        'Can you sit at ease and feel relaxed?',
        'Do you feel as if you are slowed down?',
        'Do you have a sort of frightened feeling, like with butterflies in your stomach?',
        'Have you lost interest in your appearance?',
        'Do you feel restless as if you need to be on the move?',
        'Do you look forward to things with enjoyment?',
        'Are you getting sudden feelings of panic?',
        'Can you enjoy a good book, radio, or TV program?',
    ]
    session.attributes['question_counter'] = -1 # To keep it from starting at question one
    session.attributes['total_score'] = 0
    session.attributes['points_array'] = []

    welcome_message = 'Notifying your personal contacts now... I\'m here with you Ryan. Can I ask you a few questions about how you\'re feeling?'
    send_sms('default')
    return question(welcome_message)

@ask.intent("ZeroIntent")
def zero_intent():
    question_counter = session.attributes['question_counter']
    question_array = session.attributes['question_array']
    if question_counter < len(question_array) - 1:

         # Move to the next question
         question_counter += 1
         session.attributes['question_counter'] = question_counter
         session.attributes['points_array'].append(0)

         question_text = question_array[question_counter]

         # Ask next question
         return question(question_text)
    #return statement('Questionaire completed with a total score of {}'.format(session.attributes['total_score']))
    alexaToDb(session.attributes['points_array'])
    return statement('Thank you Ryan, you did excellent. Always remember your loved ones are just a phone call away.')

@ask.intent("OneIntent")
def one_intent():
    question_counter = session.attributes['question_counter']
    question_text = session.attributes['question_array']
    if question_counter < len(question_text) - 1:

        # Move to the next question
        question_counter += 1
        session.attributes['question_counter'] = question_counter
        session.attributes['points_array'].append(1)

        # Increment score
        session.attributes['total_score'] += 1
        question_text = question_text[question_counter]

        # Ask next question
        return question(question_text)
    # Questionaire completed
    #return statement('Questionaire completed with a total score of {}'.format(session.attributes['total_score']))
    alexaToDb(session.attributes['points_array'])
    return statement('Thank you Ryan, you did excellent. Always remember your loved ones are just a phone call away.')

@ask.intent("TwoIntent")
def two_intent():
    question_counter = session.attributes['question_counter']
    question_text = session.attributes['question_array']
    if question_counter < len(question_text) - 1:

        # Move to the next question
        question_counter += 1
        session.attributes['question_counter'] = question_counter
        session.attributes['points_array'].append(2)

        # Increment score
        session.attributes['total_score'] += 2
        question_text = question_text[question_counter]

        # Ask next question
        return question(question_text)
    # Questionaire completed
    #return statement('Questionaire completed with a total score of {}'.format(session.attributes['total_score']))
    alexaToDb(session.attributes['points_array'])
    return statement('Thank you Ryan, you did excellent. Always remember your loved ones are just a phone call away.')

@ask.intent("ThreeIntent")
def three_intent():
    question_counter = session.attributes['question_counter']
    question_text = session.attributes['question_array']
    if question_counter < len(question_text) - 1:

        # Move to the next question
        question_counter += 1
        session.attributes['question_counter'] = question_counter
        session.attributes['points_array'].append(3)

        # Increment score
        session.attributes['total_score'] += 3
        question_text = question_text[question_counter]

        # Ask next question
        return question(question_text)
    # Questionaire completed
    #return statement('Questionaire completed with a total score of {}'.format(session.attributes['total_score']))
    alexaToDb(session.attributes['points_array'])
    # Thank you Ryan, you did excellent. I\'m here if you would like to listen to music, talk, or even learn something new.
    return statement('Thank you Ryan, you did excellent. Always remember your loved ones are just a phone call away.')

@ask.intent("EmergencyIntent")
def emergency_intent():
    send_sms('emergency')
    return statement('You are loved, Ryan. Don\'t worry, I am with you. Emergency services have been contacted, help is on the way.')

@ask.intent("UnknownIntent")
def unkown_intent():
    question_counter = session.attributes['question_counter']
    question_text = session.attributes['question_array'][question_counter]
    return question('Sorry, I didn\'t understand what you said,' + question_text)

@ask.session_ended
def session_ended():
    send_sms('no_response')
    return '{}', 200

@ask.intent("NoIntent")
def no_intent():
    return statement("Never gonna give you up, never gonna let you down R2D2")

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
