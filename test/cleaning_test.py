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

def test_reduce_market():
    df = reduce_market_categories(companies_df)
    market_nums = len(df['market'].unique())
    assert(market_nums == final_num_markets)

def test_reduce_countries():
    initial_features = companies_df.shape[1]
    df = company_country_features(companies_df)
    print(df.columns)
    new_features = df.shape[1]
    assert((new_features - initial_features + 1) == final_num_countries)

def test_dates_imputed():
    return

# def temporal_datatypes():
#     return



#
#
#
#
#
#
#
# # Read in data to test aquastat with.
# aquastat_df = pd.read_csv('aquastat.csv')
#
# # Time period to test functions with.
# test_time_period = '2003-2007'
#
# # Country to test functions with.
# test_country = 'Portugal'
#
# # Variable to test functions with.
# test_variable = 'permanent_crop_area'
#
# # Dataframe to test time_slice.
# test_time_slice_df = aquastat_df[aquastat_df.time_period == test_time_period]
# test_time_slice_df = test_time_slice_df.pivot(index='country', columns='variable', values='value')
# test_time_slice_df.columns.name = test_time_period
#
# # Dataframe to test time_series.
# test_time_series = aquastat_df[(aquastat_df.country == test_country) & (aquastat_df.variable == test_variable)]
# test_time_series = test_time_series.dropna()[['year_measured', 'value']]
# test_time_series.year_measured = test_time_series.year_measured.astype(int)
# test_time_series.set_index('year_measured', inplace=True)
# test_time_series.columns = [test_variable]
#
# # Dataframe to test variable_slice.
# test_variable_slice_df = aquastat_df[aquastat_df.variable==test_variable]
# test_variable_slice_df = test_variable_slice_df.pivot(index='country', columns='time_period', values='value')
#
# # Tests for time_slice()
#
# # Test for whether time period selected matches.
# def test_time_slice_time_period():
#     test_df = time_slice(aquastat_df, test_time_period)
#     assert test_df.columns.name == test_time_period
#
# # Test for whether columns match all variables.
# def test_time_slice_columns():
#     test_df = time_slice(aquastat_df, test_time_period)
#     variable_list = aquastat_df['variable'].unique()
#     variable_list.sort()
#     assert (test_df.columns == variable_list).all()
#
# # Test for whether dataframe values match.
# def test_time_slice_data():
#     test_df = time_slice(aquastat_df, test_time_period)
#     pdt.assert_frame_equal(test_df, test_time_slice_df)
#
# # Tests for time_series()
#
# # Test that variable series is being created for is accurate.
# def test_time_series_variable():
#     test_series = time_series(aquastat_df, test_country, test_variable)
#     assert test_series.columns == test_variable
#
# # Test for whether dataframe values match.
# def test_time_series_data():
#     test_series = time_series(aquastat_df, test_country, test_variable)
#     pdt.assert_frame_equal(test_series, test_time_series)
#
# # Tests for variable_slice()
#
# def test_variable_slice_data():
#     test_df = variable_slice(aquastat_df, test_variable)
#     pdt.assert_frame_equal(test_df, test_variable_slice_df)
