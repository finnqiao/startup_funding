import logging
import os
import re
import argparse
import pickle

import yaml
import pandas as pd
import boto3
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from helpers import gen_helpers as gen_h

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def data_filter(file_path, selected_features):
    """Loads data from filepath and only returns selected features based on RFE
    Args:
        file_path (str): filepath where aggregated csv file is
        selected_features (list): list of selected features from previous RFE run
    Returns:
        df (dataframe): Dataframe with filtered features
    """
    df = pd.read_csv(file_path)

    return df[selected_features]

def fit_model(df, target, test_size, hyperparams):
    """Splits data into train and test and runs a random forest which has been
    tuned previously with GridSearchCV
    Args:
        df (dataframe): filtered dataframe with selected features
        target (string): target feature expressed as a string
        test_size (float): portion of data used as test set
        hyperparams (dict): dictionary of hyperparams derived from GridSearchCV
    Returns:
        model (model): trained random forest model ready to save to pickle file
    """

    X = df.drop(target, axis=1)
    y = np.log(df[target] + 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    regressor = RandomForestRegressor(**hyperparams)
    regressor.fit(X_train, y_train)

    return regressor

def run_training(args):
    """Loads config, loads aggregated data file, filters by selected features,
    and trains a random forest regression.
    Args:
        args
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = data_filter(args.input_file_path, config['train_model']['data_filter']['selected_features'])

    model = fit_model(df, config['train_model']['fit_model']['target'],
                    config['train_model']['fit_model']['test_size'],
                    config['train_model']['fit_model']['hyperparams'])

    # Save pickle locally to models folder
    with open(args.save, "wb") as f:
        pickle.dump(model, f)
    logger.info("Trained model object saved to %s", args.save)

    # Save pickle to S3 bucket
    s3 = boto3.client("s3")
    s3.upload_file(args.save, args.bucket_name, args.output_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument("--input_file_path", default='data/auxiliary/aggregated_data.csv',
        help="input file path to aggregated data")
    parser.add_argument('--save', default='models/sample_model.pkl',
        help='path to where the model should be saved to')
    parser.add_argument("--bucket_name", default='startup-funding-working-bucket',
        help="S3 bucket name")
    parser.add_argument("--output_file_path", default='sample_model.pkl',
        help="output file path of uploaded file in s3 bucket")

    args = parser.parse_args()

    run_training(args)

# makefile command
# python src/train_model.py --config=config/model_config.yml --save=models/sample_model.pkl
