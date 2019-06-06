import pytest
import pandas as pd
import pandas.util.testing as pdt
import os
import sys
import logging
sys.path.append(os.path.abspath('./src'))
from helpers.gen_helpers import filter_columns, generate_onehot_features, invert_dict

logging.basicConfig(level=logging.DEBUG, filename="test_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

# Dataframe to test with.
companies_df = pd.read_csv('data/external/companies.csv')
filtered_cols = ['permalink', 'founded_at']
na_cols = ['founded_at']

len(companies_df['state_code'].unique())

test_dict = {1:['a','b'], 2:['c','d']}
result_dict = {'a':1, 'b':1, 'c':2, 'd':2}

# Test if columns are filtered.
def test_filter_columns():
    df = filter_columns(companies_df, filtered_cols, na_cols)
    assert(len(df.columns) == 2)

# Test if na rows are dropped from subset columns.
def test_filter_na():
    df = filter_columns(companies_df, filtered_cols, na_cols)
    assert(df['founded_at'].isnull().sum() == 0)

# Test if one hot columns were generated.
def test_onehot():
    df = generate_onehot_features(companies_df, 'state_code')
    assert((df.shape[1] - companies_df.shape[1] + 1) == 61)

# Test for dictionary inversion.
def test_dict_invert():
    assert(invert_dict(test_dict) == result_dict)
