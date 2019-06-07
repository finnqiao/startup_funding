import traceback
from flask import render_template, request, redirect, url_for
import logging.config
# from app.models import Tracks
from flask import Flask
# from src.add_songs import Tracks
from flask_sqlalchemy import SQLAlchemy
import pickle
import sklearn
import pandas as pd

# Initialize the Flask application
# app = Flask(__name__)

# Configure flask app from flask_config.py
# app.config.from_pyfile('config/flask_config.py')

# Initialize the database
# db = SQLAlchemy(app)

# Use pickle to load in the pre-trained model
with open('models/sample_model.pkl', 'rb') as f:
    model = pickle.load(f)

# @app.route('/')
# def index():
#     """Title view"""
#     return render_template('index.html')
#
# @app.route('/main', methods=['POST'])
# def main():
#     """Page with form to submit to model for prediction"""
#
#     return render_template(url_for('index'))



all_features = ['funding_rounds', 'founded_month', 'founded_quarter', 'founded_year',
'country_esp', 'country_ind', 'country_other', 'country_usa', 'days_to_fund', 'months_to_fund',
'days_between_rounds', 'months_between_rounds', 'funding_round_type_debt_financing',
'funding_round_type_post_ipo_debt', 'funding_round_type_post_ipo_equity',
'funding_round_type_private_equity', 'funding_round_type_venture', 'unique_investors',
'median_investor_value', 'no_acquisitions', 'no_ipos', 'market_biotechnology',
'market_clean technology', 'market_enterprise software', 'market_finance', 'market_health and wellness',
'market_hospitality', 'market_internet', 'market_mobile', 'market_other']
model_input = dict.fromkeys(all_features, [0])
model_input = pd.DataFrame.from_dict(model_input)
predict = model.predict(model_input)
print(predict[0])

import pandas as pd
df = pd.read_csv('data/auxiliary/aggregated_data.csv')
df = df[all_features]
df.describe()
