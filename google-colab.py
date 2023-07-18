!pip install flask_ngrok

import pandas as pd
from flask_ngrok import run_with_ngrok
from flask import request, jsonify, Flask
import random as r

app = Flask(__name__)
run_with_ngrok(app)

people = [
  {
    'number': '1',
    'name': 'mahesh',
    'age': 25,
    'city': 'bangalore',
    'country': 'india'
  },
  {
    'number': '2',
    'name': 'alex',
    'age': 26,
    'city': 'london',
    'country': 'uk'
  },
  {
    'number': '3',
    'name': 'david',
    'age': 27,
    'city': 'san francisco',
    'country': 'usa'
  },
  {
    'number': '4',
    'name': 'john',
    'age': 28,
    'city': 'toronto',
    'country': 'canada'
  },
  {
    'number': '5',
    'name': 'chris',
    'age': 29,
    'city': 'paris',
    'country': 'france'
  }
]

@app.route('/')
def input():
  return jsonify(people)

@app.route('/list', methods=['GET', 'POST'])
def predJSON():
  pred = r.choice(['positive', 'negative'])
  nd = people
  nd['prediction'] = pred
  return jsonify(nd)

app.run()