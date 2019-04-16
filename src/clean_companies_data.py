import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import missingno as msno

# Import and inspect initial data on companies.
company_df = pd.read_csv('./data/external/companies.csv')

company_df.head()

# Visualize missing values in data.
msno.matrix(company_df)

# List of columns for companies dataframe.
company_df.columns
