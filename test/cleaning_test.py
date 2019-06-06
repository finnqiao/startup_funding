import pytest
import pandas as pd
import pandas.util.testing as pdt
import os
import sys
import logging
sys.path.append(os.path.abspath('./src'))
from clean_companies_data import reduce_market_categories, company_country_features, impute_founding_date, temporal_features
from clean_acquisitions_data import get_acquisition_count
from clean_investors_data import bin_investors, get_unique_investors
from clean_rounds_data import group_permalink_funding

logging.basicConfig(level=logging.DEBUG, filename="test_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

# Read in data to test with.
companies_df = pd.read_csv('data/external/companies.csv')
acquisitions_df = pd.read_csv('data/external/acquisitions.csv')
investments_df = pd.read_csv('data/external/investments.csv')
rounds_df = pd.read_csv('data/external/rounds.csv')

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

# Test to see if all unique acquirers.
def test_unique_acquirers():
    df = get_acquisition_count(acquisitions_df, 'data/external/companies.csv')
    acq_list = list(df['permalink'])
    assert(len(acq_list) == len(set(acq_list)))

# Test to check whether labels are in deciles.
def test_investor_bins():
    df = bin_investors(investments_df)
    assert(len(list(df['bins_amount'].unique())) == 11)

# Test to check whether companies belong to initial company list.
def test_unique_investors():
    df = bin_investors(investments_df)
    df = get_unique_investors(df, 'data/external/companies.csv')

    all_companies_list = list(companies_df['permalink'].unique())
    invested_companies_list = list(df['company_permalink'].unique())
    assert(set(invested_companies_list).issubset(all_companies_list) == True)
