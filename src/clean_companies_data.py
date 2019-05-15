import logging
import os
import re
import argparse

import yaml
import pandas as pd
import numpy as np
import datetime
import boto3

from helpers import gen_helpers as gen_h
from helpers import nlp_helpers as nlp_h

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def reduce_market_categories(df):
    """Reduce market categories to top 50 and other with nlp techniques"""
    # Save list of all market types.
    market_types = list(df['market'].unique())

    # Save list of top 50 market types by company counts.
    top_50_markets = list(df['market'].value_counts().nlargest(50).index)

    outside_50_markets = [x for x in market_types if x not in top_50_markets]

    # Create dictionary of top 50 markets.
    top_50_dict = dict.fromkeys(top_50_markets)

    # First pass at collapsing market categories.
    # Done by checking if first word in a category is present in other category
    # labels.
    # Example 1: word "advertising" apppears in "advertising platforms".
    # Example 2: "enterprise" is the first word in "enterprise software"
    # appears in "enterprise 2.0"

    for key in top_50_dict.keys():
        # Initialize each key with empty list
        top_50_dict[key] = []
        for cat in outside_50_markets:
            # Check if first word is present in category, add to key value list,
            # remove from category list.
            if key.split(' ')[0] in cat.split(' '):
                top_50_dict[key].append(cat)
                outside_50_markets.remove(cat)
            elif ((len(key.split(' ')) > 1) and (key.split(' ')[1] == 'and')
            and (key.split(' ')[2] in cat.split(' '))):
                top_50_dict[key].append(cat)
                outside_50_markets.remove(cat)

    # Check how many categories are left.
    remainder_outside_50 = outside_50_markets

    # Second pass at collapsing market categories.
    # Market category labels are split into character n-grams.
    # N-gram similarity Dice metric is calculated with intersection/union of
    # n-gram sets.
    for key in top_50_dict.keys():
        for cat in remainder_outside_50:
            if nlp_h.sim4gram(key, cat) > 0.25:
                top_50_dict[key].append(cat)
                remainder_outside_50.remove(cat)

    # Assign remainder of categories to "Other"
    top_50_dict['other'] = remainder_outside_50

    # Invert keys and values
    category_replace_dict = gen_h.invert_dict(top_50_dict)

    # Relabel key value pairs that do not match well.
    category_replace_dict['big data analytics'] = 'big data'
    category_replace_dict['coworking'] = 'other'
    category_replace_dict['mining technologies'] = 'other'
    category_replace_dict['mobility'] = 'other'
    category_replace_dict['nanotechnology'] = 'other'
    category_replace_dict['real time'] = 'other'
    category_replace_dict['space travel'] = 'other'
    category_replace_dict['social network media'] = 'social media'

    # Replace values in market column based on replacement dictionary.
    df['market'] = df['market'].map(category_replace_dict).fillna(df['market'])

    return df

# def generate_onehot_features(df, column):
#     """Generate one-hot encoding of selected column"""
#     df[column].value_counts()
#
#     df = pd.concat([df, pd.get_dummies(df[column], prefix=column)], axis=1)
#     df = df.drop(column, axis=1)
#
#     return df

def company_country_features(df):
    """Generate one-hot encoding of top countries and others"""
    #  Countries with startup numbers above global mean.
    top_countries = list(df['country_code'].value_counts()[df['country_code']
    .value_counts() > df['country_code'].value_counts().mean()].index)

    # Replace other countries with 'other'.
    df['country_code'] = df['country_code'].fillna('other')
    df.loc[~df['country_code'].isin(top_countries), 'country_code'] = 'other'

    # One-hot encoding of countries.
    df = pd.concat([df, pd.get_dummies(df['country_code'], prefix='country')], axis=1)
    df = df.drop('country_code', axis=1)

    return df

def impute_founding_date(df):
    """Impute missing founding dates."""
    # Convert datetime columns to datetime objects.
    df['first_funding_at'] = pd.to_datetime(df['first_funding_at'], errors='coerce')
    df['last_funding_at'] = pd.to_datetime(df['last_funding_at'], errors='coerce')
    df['founded_at'] = pd.to_datetime(df['founded_at'], errors='coerce')

    # Save two date columns in new dataframe to calculate median value.
    median_days_to_fund = np.median(((df['first_funding_at'] - df['founded_at'])
    /(np.timedelta64(1, 'D'))).dropna())

    # Impute NAs for founded_at by subtracting median_days_to_fund to first_funding_at.
    df['founded_at'] = df['founded_at'].fillna(df['first_funding_at'] -
    datetime.timedelta(days = median_days_to_fund))

    # Filling in founded date features based on imputed values.
    df['founded_year'] = df['founded_at'].dt.year
    df['founded_month'] = df['founded_at'].dt.month
    df['founded_quarter'] = df['founded_month'].map({1:1,2:1,3:1,4:2,5:2,6:2,
    7:3,8:3,9:3,10:4,11:4,12:4})

    return df

def temporal_features(df):
    """Feature generation for temporal features."""

    # Number of days and months from first founding date that first round was raised.
    df['days_to_fund'] = ((df['first_funding_at'] - df['founded_at'])/
    (np.timedelta64(1, 'D')))
    df['months_to_fund'] = ((df['first_funding_at'] - df['founded_at'])/
    (np.timedelta64(1, 'M')))

    # Number of days and months between funding rounds.
    df['days_between_rounds'] = ((df['last_funding_at'] - df['first_funding_at'])/
    (np.timedelta64(1, 'D'))/df['funding_rounds'])
    df['months_between_rounds'] = ((df['last_funding_at'] - df['first_funding_at'])/
    (np.timedelta64(1, 'M'))/df['funding_rounds'])

    # If only a single round, use value of days or months to first funding.
    df.loc[df['days_between_rounds'] == 0, 'days_between_rounds'] = df['days_to_fund']
    df.loc[df['months_between_rounds'] == 0, 'months_between_rounds'] = df['months_to_fund']

    return df

def run_clean_companies(args):
    """Loads config and cleans the companies dataset. Uses cleaned data to
    generate new features.
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level
            key containing relevant configurations
            args.save (str): If given, resulting dataframe will be saved to this
            location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = gen_h.read_data(args.input_file)
    df = gen_h.filter_columns(df, **config['clean_companies_data']['filter_columns'])
    df = reduce_market_categories(df)
    df = gen_h.generate_onehot_features(df, **config['clean_companies_data']
    ['generate_onehot_features'])
    df = company_country_features(df)
    df = impute_founding_date(df)
    df = temporal_features(df)

    # Save working copy to local
    df.to_csv(args.save)

    # Save copy to S3 Bucket
    s3 = boto3.client("s3")
    s3.upload_file(args.save, args.bucket_name, args.output_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input_file', help='path to csv file with raw data')
    parser.add_argument('--save', default='data/auxiliary/new_companies_data.csv',
    help='path to where the cleaned dataset should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
    help="S3 bucket name")
    parser.add_argument("--output_file_path", default='new_companies_data.csv',
    help="output file path of uploaded file")

    args = parser.parse_args()

    run_clean_companies(args)

# makefile command
# python src/clean_companies_data.py --config=config/model_config.yml --input_file=data/external/companies.csv --save=data/auxiliary/new_companies_data.csv
