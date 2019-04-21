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

# First pass at collapsing market categories.
# Done by checking if first word in a category is present in other category labels.
# Example 1: word "advertising" apppears in "advertising platforms".
# Example 2: "enterprise" is the first word in "enterprise software" apppears in "enterprise 2.0"

for key in tqdm(top_50_dict.keys()):
    # Initialize each key with empty list
    top_50_dict[key] = []
    for cat in outside_50_markets:
        # Check if first word is present in category, add to key value list, remove from category list.
        if key.split(' ')[0] in cat.split(' '):
            top_50_dict[key].append(cat)
            outside_50_markets.remove(cat)
        elif (len(key.split(' ')) > 1) and (key.split(' ')[1] == 'and') and (key.split(' ')[2] in cat.split(' ')):
            top_50_dict[key].append(cat)
            outside_50_markets.remove(cat)

# Check how many categories are left.
remainder_outside_50 = outside_50_markets
len(remainder_outside_50)

# Second pass at collapsing market categories.
# Market category labels are split into character n-grams.
# N-gram similarity Dice metric is calculated with intersection/union of n-gram sets.

def word2ngrams(text, n=4, exact=True):
    """Convert text into ngrams."""
    return ["".join(g) for g in zip(*[text[i:] for i in range(n)])]

def sim4gram(text1, text2):
    """Calculate ngram similarity metric."""
    list1 = word2ngrams(text1)
    list2 = word2ngrams(text2)
    return len(list(set(list1) & set(list2)))/len(list(set(list1) | set(list2)))

for key in tqdm(top_50_dict.keys()):
    for cat in remainder_outside_50:
        if sim4gram(key, cat) > 0.25:
            top_50_dict[key].append(cat)
            remainder_outside_50.remove(cat)

# Check how many categories are left.
len(remainder_outside_50)

# Assign remainder of categories to "Other"
top_50_dict['other'] = remainder_outside_50

def invert_dict(d):
    """Function to invert a dictionary of lists so list values become keys."""
    return dict( (v,k) for k in d for v in d[k] )

category_replace_dict = invert_dict(top_50_dict)

# Relabel key value pairs that do not match well.
category_replace_dict['big data analytics'] = 'big data'
category_replace_dict['coworking'] = 'other'
category_replace_dict['mining technologies'] = 'other'
category_replace_dict['mobility'] = 'other'
category_replace_dict['nanotechnology'] = 'other'
category_replace_dict['real time'] = 'other'
category_replace_dict['space travel'] = 'other'
category_replace_dict['social network media'] = 'social media'

# Replace values in market column based on replacement dictionary.
company_df['market'] = company_df['market'].map(category_replace_dict).fillna(company_df['market'])

# One-hot encoding of startup status.
company_df['status'].value_counts()

company_df = pd.concat([company_df, pd.get_dummies(company_df['status'], prefix='status')], axis=1)
company_df = company_df.drop('status', axis=1)
company_df.head()


# Countries with startup numbers above global mean.
list(company_df['country_code'].value_counts()[company_df['country_code'].value_counts() > company_df['country_code'].value_counts().mean()].index)

# Replace other countries with 'other'.

# One-hot encoding of countries.






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
