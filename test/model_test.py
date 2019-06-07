import pytest
import pandas as pd
import pandas.util.testing as pdt
import os
import sys
import logging
sys.path.append(os.path.abspath('./src'))
from train_model import data_filter

logging.basicConfig(level=logging.DEBUG, filename="test_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

selected_features = ['funding_rounds', 'founded_month', 'founded_quarter', 'founded_year',
'country_esp', 'country_ind', 'country_other', 'country_usa', 'days_to_fund', 'months_to_fund',
'days_between_rounds', 'months_between_rounds', 'funding_round_type_debt_financing',
'funding_round_type_post_ipo_debt', 'funding_round_type_post_ipo_equity',
'funding_round_type_private_equity', 'funding_round_type_venture', 'unique_investors',
'median_investor_value', 'no_acquisitions', 'no_ipos', 'market_biotechnology',
'market_clean technology', 'market_enterprise software', 'market_finance', 'market_health and wellness',
'market_hospitality', 'market_internet', 'market_mobile', 'market_other', 'raised_amount_usd_mean']

agg_df = pd.read_csv('data/auxiliary/aggregated_data.csv')

def test_filter():
    df = data_filter(agg_df, selected_features)
    assert(list(df.columns) == selected_features)
