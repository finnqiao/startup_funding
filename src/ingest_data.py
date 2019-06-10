import logging
import os
import re
import argparse

import glob
import boto3
import yaml
import pandas as pd

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

def get_s3_file_names(s3_prefix_path):
    """Get all file names in an s3 bucket under a prefix
    Args:
        s3_prefix_path (str): S3 path to prefix containing all files to list
    Returns: List of all S3 file locations
    """

    # Parse out s3 bucket name using regex from input string
    regex = r"s3:\/\/([\w._-]+)\/"
    m = re.match(regex, s3_prefix_path)
    s3bucket_name = m.group(1)
    logging.info('Bucket name parsed out is %s', s3bucket_name)

    # Get s3 bucket handle
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(s3bucket_name)

    files = []
    for object in s3bucket.objects.all():
        path_to_file = os.path.join("s3://%s" % s3bucket_name, object.key)
        logging.debug('File with path %s is being added', path_to_file)
        files.append(path_to_file)

    return files


def get_file_names(top_dir):
    """Get all file names in a directory subtree
    Args:
        top_dir (str): The base directory from which to get list_of_files from
    Returns: List of file locations
    """

    if top_dir.startswith("s3://"):
        list_of_files = get_s3_file_names(top_dir)
    else:
        top_dir = top_dir[:-1] if top_dir[-1] == "/" else top_dir
        list_of_files = glob.glob(top_dir+'/*.csv', recursive=True)

    return list_of_files

def load_csv(path, **kwargs):
    """Wrapper function for `pandas.read_csv()` method to enable multiprocessing.
    """
    return pd.read_csv(path, **kwargs)

def load_csvs(file_names=None, directory=None):
    """Loads multiple CSVs into a single Pandas dataframe.
    Given either a directory name (which can be local or an s3 bucket prefix)
    or a list of CSV files, this function
    will load all CSVs into a single Pandas DataFrame. It assumes the same
    schema exists across all CSVs.

    Args:
        file_names (list of str, default=None): List of files to load.
        If None, `directory` should be given.
        directory (str, default=None): Directory containing files to be loaded.
        If None, `filenames` should be given.
    Returns: Single dataframe with data from all files loaded
    """

    # Get list of files
    if file_names is None and directory is None:
        raise ValueError("filenames or directory must be given")
    elif file_names is None:
        file_names = get_file_names(directory)

    df_list = [(file_name.split('/')[-1], load_csv(file_name)) for file_name in file_names]

    return df_list

def run_loading(args):
    """Loads config and executes load data set
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level key
            containing relevant configurations
            args.save (str): If given, resulting dataframe will be saved to this
            location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df_list = load_csvs(**config["ingest_data"]["load_csvs"])

    for df in df_list:
        df[1].to_csv(args.save + df[0])
        logging.debug('Dataframe saved to %s', args.save)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--save', default='data/external/',
    help='Path to where the dataset should be saved to')

    args = parser.parse_args()

    run_loading(args)

# makefile command
# python src/ingest_data.py --config=config/model_config.yml --save=data/external/
