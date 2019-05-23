import logging
import os
import re
import argparse

import yaml
import pandas as pd
import numpy as np
import boto3

from helpers import gen_helpers as gen_h

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def bin_investors(df):
    """Group investors by investor key and obtain summary statistics for investment amounts."""
    investors_amount_df = df.groupby('investor_permalink').agg(
    {'raised_amount_usd':['sum','mean','median','min','max']}).dropna()
    investors_amount_df.columns =  ['_'.join(col).strip() for col in
    investors_amount_df.columns.values]

    # Bin investors into deciles based on total investment amounts.
    investors_amount_df['bins_amount'] = pd.qcut(investors_amount_df
    ['raised_amount_usd_sum'].values, 10).codes
    investors_amount_df = investors_amount_df.reset_index()

    # Merge investor bin into df
    df = pd.merge(df, investors_amount_df[
    ['investor_permalink','bins_amount']], how='left',
    left_on='investor_permalink', right_on='investor_permalink')

    return df

def get_unique_investors(df, all_companies_file):
    """Get number of unique investors that invested in each company and median value"""
    company_df = pd.read_csv(all_companies_file)

    # Get number of unique investors and mean investor bin quality (decile)
    all_companies_list = list(company_df['permalink'].unique())

    # Filtes unique investors such that only those investing in companies listed in
    # the initial companies df are included
    unique_investors_df = df.groupby('company_permalink').agg(
    {'investor_permalink':pd.Series.nunique,
    'bins_amount': np.median}).reset_index()
    unique_investors_df = unique_investors_df[unique_investors_df
    ['company_permalink'].isin(all_companies_list)]

    unique_investors_df = unique_investors_df.fillna(0)
    unique_investors_df.columns = ['company_permalink','unique_investors',
    'median_investor_value']

    return unique_investors_df

def run_clean_investors(args):
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

    df = pd.read_csv(args.input_file)
    df = bin_investors(df)
    df = get_unique_investors(df, **config['clean_investors_data']['get_unique_investors'])

    df.to_csv(args.save)

    # Save copy to S3 Bucket
    s3 = boto3.client("s3")
    s3.upload_file(args.save, args.bucket_name, args.output_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input_file', help='path to csv file with raw data')
    parser.add_argument('--save', default='data/auxiliary/new_investors_data.csv',
    help='path to where the cleaned dataset should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
    help="S3 bucket name")
    parser.add_argument("--output_file_path", default='new_investors_data.csv',
    help="output file path of uploaded file")

    args = parser.parse_args()

    run_clean_investors(args)

# makefile command
# python src/clean_investors_data.py --config=config/model_config.yml --input_file=data/external/investments.csv --save=data/auxiliary/new_investors_data.csv
