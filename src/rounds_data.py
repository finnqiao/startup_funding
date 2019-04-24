import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import missingno as msno
import collections
import itertools
from tqdm import tqdm
import nltk
from datetime import datetime, timedelta

# Import and inspect initial data on companies.
rounds_df = pd.read_csv('./data/external/rounds.csv')

rounds_df.head()

# Choose non-overlapping columns with companies dataframe.
rounds_df = rounds_df[['company_permalink', 'funding_round_type', 'raised_amount_usd']]

# Drop undisclosed funding rounds.
rounds_df = rounds_df.dropna()

# Get dummy variables for all funding round types.
rounds_df = pd.concat([rounds_df, pd.get_dummies(rounds_df['funding_round_type'], prefix='round_type')], axis=1)
rounds_df = rounds_df.drop('funding_round_type', axis=1)

# Get total number of funding rounds for each funding round type.
round_type_df = rounds_df.groupby('company_permalink').agg('sum')

# Get summary statistics for funding round amounts.
amounts_df = rounds_df.groupby('company_permalink').agg({'raised_amount_usd':['mean','median','max','min']})
amounts_df.columns = ['_'.join(col).strip() for col in amounts_df.columns.values]

# Join round type and fund amount type data.
# Cleaned and feature engineered version for venture rounds.
venture_rounds_df = rounds_df.join(amounts_df, on='company_permalink')
