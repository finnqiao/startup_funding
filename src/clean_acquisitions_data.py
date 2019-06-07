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

def get_acquisition_count(df, all_companies_file):
    """Aggregates acquisition by acquirer and creates new dataframe for
    acquisition count"""
    # Create list of acquired companies in original company dataset
    company_df = pd.read_csv(all_companies_file)
    all_companies_list = list(company_df['permalink'].unique())
    acquired_companies_list = list(df['company_permalink'].unique())
    acquirer_companies_list = list(df['acquirer_permalink'].unique())
    logging.info('There are %s number of acquired companies', len(acquired_companies_list))
    logging.info('There are %s number of acquirer companies', len(acquirer_companies_list))

    acquired_companies_list = [permalink for permalink in acquired_companies_list
    if permalink in all_companies_list]
    acquirer_companies_list = [permalink for permalink in acquirer_companies_list
    if permalink in all_companies_list]

    # Create dictionary of number of acquisitions by acquirers that are in original company dataset
    acquirer_dict = dict(df['acquirer_permalink'].value_counts())
    acquirer_dict = {acquirer: acquirer_dict[acquirer] for acquirer in acquirer_dict
    if acquirer in acquirer_companies_list}

    # Create dataframe of number of acquisitions to merge into other dataframes
    acquirers_df = pd.DataFrame.from_dict(acquirer_dict, orient='index').reset_index()
    acquirers_df.columns = ['permalink', 'no_acquisitions']
    return acquirers_df

def run_clean_acquisitions(args):
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
    df = get_acquisition_count(df, **config['clean_acquisitions_data']
    ['get_acquisition_count'])

    df.to_csv(args.save)
    logging.debug('Working copy was saved to %s', args.save)

    # Save copy to S3 Bucket
    if args.bucket_name != None:
        s3 = boto3.client("s3")
        s3.upload_file(args.save, args.bucket_name, args.output_file_path)
        logging.debug('Working copy was saved to bucket %s', args.bucket_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input_file', help='path to csv file with raw data')
    parser.add_argument('--save', default='data/auxiliary/new_acquisitions_data.csv',
    help='path to where the cleaned dataset should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
    help="S3 bucket name")
    parser.add_argument("--output_file_path", default='new_acquisitions_data.csv',
    help="output file path of uploaded file")

    args = parser.parse_args()

    run_clean_acquisitions(args)

# makefile command
# python src/clean_acquisitions_data.py --config=config/model_config.yml --input_file=data/external/acquisitions.csv --save=data/auxiliary/new_acquisitions_data.csv
