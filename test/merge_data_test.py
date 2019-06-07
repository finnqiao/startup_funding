import pytest
import pandas as pd
import pandas.util.testing as pdt
import os
import sys
import logging
import pandas.util.testing as pdt
sys.path.append(os.path.abspath('./src'))
from preprocess_merge_data import aggregate_dataframes
from helpers import gen_helpers as gen_h

logging.basicConfig(level=logging.DEBUG, filename="test_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

data_paths = [
'data/auxiliary/new_companies_data.csv','data/auxiliary/new_rounds_data.csv',
'data/auxiliary/new_investors_data.csv','data/auxiliary/new_acquisitions_data.csv',
'data/auxiliary/new_ipo_data.csv'
]

for data_path in data_paths:
    if 'companies' in data_path:
        companies_df = pd.read_csv(data_path)
    elif 'investors' in data_path:
        investors_df = pd.read_csv(data_path)
    elif 'rounds' in data_path:
        rounds_df = pd.read_csv(data_path)
    elif 'acquisitions' in data_path:
        acquisitions_df = pd.read_csv(data_path)
    elif 'ipo' in data_path:
        ipo_df = pd.read_csv(data_path)

# Combine companies_df, rounds_df, investors_df, acquisitions_df, ipo_df
agg_df = pd.merge(companies_df, rounds_df, how='left', left_on='permalink',
    right_on='company_permalink')
agg_df = pd.merge(agg_df, investors_df, how='left', left_on='permalink',
    right_on='company_permalink')
agg_df = pd.merge(agg_df, acquisitions_df, how='left', left_on='permalink',
    right_on='permalink')
agg_df = pd.merge(agg_df, ipo_df, how='left', left_on='founded_year',
    right_on='year')
agg_df = agg_df.drop(['name','category_list','founded_at','first_funding_at',
    'last_funding_at','company_permalink_x', 'company_permalink_y', 'year'],axis=1)

agg_df = agg_df.fillna(0)

# Test to check if cleaned data was merged properly.
def test_merging():
    df = aggregate_dataframes(data_paths)
    pdt.assert_frame_equal(df, agg_df)
