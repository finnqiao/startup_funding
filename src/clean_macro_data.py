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

def run_ipo(args):
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

    df = pd.read_csv(args.input_file, index_col=0)
    df.columns = ['year','no_ipos']
    logging.info('There are %s years of ipo data', df.shape[0])

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
    parser.add_argument('--save', default='data/auxiliary/new_ipo_data.csv',
    help='path to where the cleaned dataset should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
    help="S3 bucket name")
    parser.add_argument("--output_file_path", default='new_ipo_data.csv',
    help="output file path of uploaded file")

    args = parser.parse_args()

    run_ipo(args)

# makefile command
# python src/clean_macro_data.py --config=config/model_config.yml --input_file=data/external/ipo_counts.csv --save=data/auxiliary/new_ipo_data.csv
