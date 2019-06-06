import pytest
import pandas as pd
import pandas.util.testing as pdt
import os
import sys
import logging
sys.path.append(os.path.abspath('./src'))
from clean_companies_data import reduce_market_categories, company_country_features, impute_founding_date, temporal_features

logging.basicConfig(level=logging.DEBUG, filename="test_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

# Read in data to test with.
companies_df = pd.read_csv('data/external/companies.csv')

final_num_markets = 52
final_num_countries = 10
final_num_temporal = 4

# Test to see if reducing markets worked and final number matches dataframe.
def test_reduce_market():
    df = reduce_market_categories(companies_df)
    market_nums = len(df['market'].unique())
    assert(market_nums == final_num_markets)

# Test to see if countries were reduced to 10 one-hot columns.
def test_reduce_countries():
    initial_features = companies_df.shape[1]
    df = company_country_features(companies_df)
    new_features = df.shape[1]
    assert((new_features - initial_features + 1) == final_num_countries)

# Test to check if date columns have been imputed.
def test_dates_imputed():
    df = impute_founding_date(companies_df)
    assert(df['founded_at'].isnull().sum() == 0)

# Test to check if temporal features have been generated.
def test_temporal_types():
    df = impute_founding_date(companies_df)
    initial_features = df.shape[1]
    df = temporal_features(df)
    new_features = df.shape[1]
    assert((new_features - initial_features) == final_num_temporal)
