import logging
import os
import re
import argparse

import yaml
import pandas as pd
import boto3

from helpers import gen_helpers as gen_h

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

def group_permalink_funding(df):
    """Generate features based on funding round descriptive statistics"""
    # Get total number of funding rounds for each funding round type.
    round_type_df = df.groupby('company_permalink').agg('sum')

    # Get summary statistics for funding round amounts.
    amounts_df = df.groupby('company_permalink').agg({'raised_amount_usd':
    ['mean','median','max','min']})
    amounts_df.columns = ['_'.join(col).strip() for col in amounts_df.columns.values]

    # Join round type and fund amount type data.
    venture_df = df.join(amounts_df, on='company_permalink')

    # Consolidate funding information by adding number of rounds in unique
    # round types.
    venture_df = venture_df.groupby('company_permalink').agg({
     'raised_amount_usd': 'first',
     'raised_amount_usd_max': 'first',
     'raised_amount_usd_mean': 'first',
     'raised_amount_usd_median': 'first',
     'raised_amount_usd_min': 'first',
     'funding_round_type_angel': 'sum',
     'funding_round_type_convertible_note': 'sum',
     'funding_round_type_debt_financing': 'sum',
     'funding_round_type_equity_crowdfunding': 'sum',
     'funding_round_type_grant': 'sum',
     'funding_round_type_post_ipo_debt': 'sum',
     'funding_round_type_post_ipo_equity': 'sum',
     'funding_round_type_private_equity': 'sum',
     'funding_round_type_product_crowdfunding': 'sum',
     'funding_round_type_secondary_market': 'sum',
     'funding_round_type_seed': 'sum',
     'funding_round_type_undisclosed': 'sum',
     'funding_round_type_venture': 'sum'})
    venture_df = venture_df.reset_index()
    logging.info('There are %s funding round types', venture_df.shape[1])

    return venture_df

def run_clean_rounds(args):
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
    df = gen_h.filter_columns(df, **config['clean_rounds_data']['filter_columns'])
    df = gen_h.generate_onehot_features(df, **config['clean_rounds_data']
    ['generate_onehot_features'])
    df = group_permalink_funding(df)

    df.to_csv(args.save)
    logging.debug('Working copy was saved to %s', args.save)

    # Save copy to S3 Bucket
    s3 = boto3.client("s3")
    s3.upload_file(args.save, args.bucket_name, args.output_file_path)
    logging.debug('Working copy was saved to bucket %s', args.bucket_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input_file', help='path to csv file with raw data')
    parser.add_argument('--save', default='data/auxiliary/new_rounds_data.csv',
    help='path to where the cleaned dataset should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
    help="S3 bucket name")
    parser.add_argument("--output_file_path", default='new_rounds_data.csv',
    help="output file path of uploaded file")

    args = parser.parse_args()

    run_clean_rounds(args)

# makefile command
# python src/clean_rounds_data.py --config=config/model_config.yml --input_file=data/external/rounds.csv --save=data/auxiliary/new_rounds_data.csv
