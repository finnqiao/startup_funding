import logging
import os
import re
import argparse

import yaml
import pandas as pd

import src.helpers.gen_helpers as gen_h

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def group_permalink_funding(df):
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
     'round_type_angel': 'sum',
     'round_type_convertible_note': 'sum',
     'round_type_debt_financing': 'sum',
     'round_type_equity_crowdfunding': 'sum',
     'round_type_grant': 'sum',
     'round_type_post_ipo_debt': 'sum',
     'round_type_post_ipo_equity': 'sum',
     'round_type_private_equity': 'sum',
     'round_type_product_crowdfunding': 'sum',
     'round_type_secondary_market': 'sum',
     'round_type_seed': 'sum',
     'round_type_undisclosed': 'sum',
     'round_type_venture': 'sum'}).reset_index()

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

    df = gen_h.read_data(args.input_file)
    df = filter_columns(df, **config['clean_rounds_data']['filter_columns'])
    df = gen_h.generate_onehot_features(df, config['clean_rounds_data']
    ['generate_onehot_features'])
    df = group_permalink_funding(df)

    df.to_csv(args.save)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input_file', help='path to csv file with raw data')
    parser.add_argument('--save', default='data/auxiliary/new_rounds_df.csv',
    help='path to where the cleaned dataset should be saved to')

    args = parser.parse_args()

    run_clean_rounds(args)

# makefile command
# python src/clean_rounds_data.py --config=config/model_config.yml --input_file=data/external/rounds.csv --save=data/auxiliary/new_rounds_data.csv
