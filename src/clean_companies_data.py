import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import missingno as msno
import collections
from sklearn.preprocessing import MultiLabelBinarizer
import itertools
from tqdm import tqdm
import nltk

# Import and inspect initial data on companies.
company_df = pd.read_csv('./data/external/companies.csv')

# Visualize missing values in data.
msno.matrix(company_df)

# Drop if market is empty
company_df = company_df.dropna(subset = ['market'])

# Basic dataframe shape and columns.
company_df.shape

company_df.columns

# Keep columns that are relevant.
company_df = company_df[['permalink', 'name', 'market', 'category_list', 'funding_total_usd', 'status', 'country_code', 'city', 'funding_rounds', 'founded_month', 'founded_quarter', 'founded_year', 'first_funding_at', 'last_funding_at']]

# Lower case if a column is of string type.
company_df = company_df.apply(lambda column: column.str.lower() if pd.api.types.is_string_dtype(column) else column)

# Check number of unique market types.
len(company_df['market'].unique())

# Save list of all market types.
market_types = list(company_df['market'].unique())

# Save list of top 50 market types by company counts.
top_50_markets = list(company_df['market'].value_counts().nlargest(50).index)

outside_50_markets = [x for x in market_types if x not in top_50_markets]

# Create dictionary of top 50 markets.
top_50_dict = dict.fromkeys(top_50_markets)

# Potential overlaps
for key in tqdm(top_50_dict.keys()):
    top_50_dict[key] = []
    for cat in outside_50_markets:
        if key.split(' ')[0] in cat.split(' '):
            top_50_dict[key].append(cat)
            outside_50_markets.remove(cat)

top_50_dict

outside_50_markets

company_df['market'].value_counts().nlargest(100)


# Convert text into ngrams.
def word2ngrams(text, n=3, exact=True):
    return ["".join(g) for g in zip(*[text[i:] for i in range(n)])]

test1 = 'blogging platforms'
test2 = 'artificial intelligence'



list1 = word2ngrams(test1)
list2 = word2ngrams(test2)

list(set(list1) & set(list2))
list(set(list1) | set(list2))

# Drop missing values for category list as imputation methods are hard to apply for one hot encoding here.
company_df = company_df.dropna(subset=['category_list'])

# Number of unique categories.
company_df['category_list'] = company_df['category_list'].apply(lambda x: [cat for cat in x.split('|') if cat != ''])

# User MultiLabelBinarizer to convert categories into one hot encoding.
mlb = MultiLabelBinarizer()
cat_one_hot = pd.DataFrame(mlb.fit_transform(company_df['category_list']), columns=mlb.classes_, index=company_df.index)
cat_one_hot.shape
cat_one_hot.head()



[(key, len(list(group))) for key, group in itertools.groupby(company_df['category_list'].sum())]

counter = collections.Counter(company_df['category_list'].sum())
len(counter)
counter.most_common(50)



















#
