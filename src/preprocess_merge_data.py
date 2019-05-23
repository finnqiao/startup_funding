import logging
import os
import re
import argparse

import yaml
import pandas as pd
import boto3

from helpers import gen_helpers as gen_h

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def aggregate_dataframes(data_path_list):
    for data_path in data_path_list:
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
    return agg_df

def run_merging(args):
    """Loads config and merges all files within a list of files into an aggregated
    dataframe
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level
            key containing relevant configurations
            args.save (str): Resulting dataframe will be saved to this
            location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = aggregate_dataframes(**config['preprocess_merge_data']['aggregate_dataframes'])
    df = gen_h.generate_onehot_features(df, **config['preprocess_merge_data']['generate_onehot_features'])

    df.to_csv(args.save)

    # Save copy to S3 Bucket
    s3 = boto3.client("s3")
    s3.upload_file(args.save, args.bucket_name, args.output_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--save', default='data/auxiliary/aggregated.csv',
        help='path to where the cleaned dataset should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
        help="S3 bucket name")
    parser.add_argument("--output_file_path", default='aggregated.csv',
        help="output file path of uploaded file in s3 bucket")

    args = parser.parse_args()

    run_merging(args)

# makefile command
# python src/preprocess_merge_data.py --config=config/model_config.yml --save=data/auxiliary/aggregated_data.csv
