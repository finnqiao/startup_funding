import logging
import pandas as pd
import numpy as np
import missingno as msno

# Read in investments dataframe.
investors_df = pd.read_csv('./data/external/investments.csv')

# Group investors by investor key and obtain summary statistics for investment amounts.
investors_amount_df = investors_df.groupby('investor_permalink').agg({'raised_amount_usd':['sum','mean','median','min','max']}).dropna()
investors_amount_df.columns =  ['_'.join(col).strip() for col in investors_amount_df.columns.values]

# Bin investors into deciles based on total investment amounts.
investors_amount_df['bins_amount'] = pd.qcut(investors_amount_df['raised_amount_usd_sum'].values, 10).codes
