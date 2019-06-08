import sys
import os
sys.path.append(os.path.abspath('./src'))
import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from sql.create_database import Funding_Prediction
from flask_sqlalchemy import SQLAlchemy
import pickle
import sklearn
import pandas as pd
import numpy as np
import math

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

# Initialize the database
db = SQLAlchemy(app)

all_features = ['funding_rounds', 'founded_month', 'founded_quarter', 'founded_year',
'country_esp', 'country_ind', 'country_other', 'country_usa', 'days_to_fund', 'months_to_fund',
'days_between_rounds', 'months_between_rounds', 'funding_round_type_debt_financing',
'funding_round_type_post_ipo_debt', 'funding_round_type_post_ipo_equity',
'funding_round_type_private_equity', 'funding_round_type_venture', 'unique_investors',
'median_investor_value', 'no_acquisitions', 'no_ipos', 'market_biotechnology',
'market_clean technology', 'market_enterprise software', 'market_finance', 'market_health and wellness',
'market_hospitality', 'market_internet', 'market_mobile', 'market_other']

months_to_fund = [61.70147230949301, 25.922503542167192, 11.992032690609665, 2.694100494876692, -576.1432472946057]
median_investor = [0, 1, 5, 9]
acquisitions_list = [0, 1, 4, 100]

# Use pickle to load in the pre-trained model
with open('models/sample_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    """Title view"""
    return render_template('index.html')

@app.route('/main', methods=['GET','POST'])
def main():
    """Page with form to submit to model for prediction"""
    if request.method == 'GET':
        # Just render the initial form, to get input
        return(render_template('main.html'))

    if request.method == 'POST':
        # Extract the input
        startup_name = request.form['startup_name']
        num_rounds = request.form['num_rounds']
        time_first_round = request.form['time_first_round']
        time_btw_round = request.form['time_btw_round']
        funding_type = request.form['funding_type']
        founding_date = request.form['founding_date']
        country = request.form['country']
        investor_type = request.form['investor_type']
        acq_type = request.form['acq_type']
        market = request.form['market']

        model_input = dict.fromkeys(all_features, [0])

        # Load in data from form in POST.
        model_input['funding_rounds'][0] = int(num_rounds)
        model_input['founded_month'][0] = int(founding_date[-2:])
        if int(founding_date[-2:]) <= 3:
            model_input['founded_quarter'][0] = 1
        elif int(founding_date[-2:]) <= 6:
            model_input['founded_quarter'][0] = 2
        elif int(founding_date[-2:]) <= 9:
            model_input['founded_quarter'][0] = 3
        elif int(founding_date[-2:]) <= 12:
            model_input['founded_quarter'][0] = 4
        model_input['founded_year'][0] = int(founding_date[:4])
        if country in all_features:
            model_input[country][0] = 1
        if funding_type in all_features:
            model_input[funding_type][0] = 1
        if market in all_features:
            model_input[market][0] = 1
        model_input['months_to_fund'][0] = months_to_fund[int(time_first_round)]
        model_input['days_to_fund'][0] = model_input['months_to_fund'][0] * 30
        model_input['months_between_rounds'][0] = int(time_btw_round)
        model_input['days_between_rounds'][0] = model_input['months_between_rounds'][0] * 30
        model_input['median_investor_value'][0] = median_investor[int(investor_type)]
        model_input['no_acquisitions'][0] = acquisitions_list[int(acq_type)]

        model_input = pd.DataFrame.from_dict(model_input)
        predict = model.predict(model_input)

        funding = '{0:,}'.format(int(math.exp(predict[0])))

        # Adding prediction details to RDS.
        prediction1 = Funding_Prediction(startup_name = startup_name,
                                        num_rounds = int(num_rounds),
                                        time_first_round = int(time_first_round),
                                        time_btw_round = int(time_btw_round),
                                        funding_type = funding_type,
                                        founding_date = founding_date,
                                        country = country,
                                        investor_type = int(investor_type),
                                        acq_type = int(acq_type),
                                        market = market,
                                        prediction = funding)
        db.session.add(prediction1)
        db.session.commit()
        logging.info("New prediction added.")

        return(render_template('main.html', result=funding))
