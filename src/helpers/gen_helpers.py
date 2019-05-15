import logging

logger = logging.getLogger(__name__)

def read_data(path):
    """Read csv file in from path after being downloaded from S3"""
    df = pd.read_csv(path)
    return df

def filter_columns(df, column_subset, na_subset):
    """Filter out irrelevant columns and drop if values are NaN for a subset of
    columns"""
    df = df[column_subset]
    df = df.dropna(subset = na_subset)
    df = df.apply(lambda column: (column.str.lower() if
    pd.api.types.is_string_dtype(column) else column))
    return df

def generate_onehot_features(df, column):
    """Generate one-hot encoding of selected column"""
    df[column].value_counts()
    df = pd.concat([df, pd.get_dummies(df[column], prefix=column)], axis=1)
    df = df.drop(column, axis=1)
    return df

def invert_dict(d):
    """Function to invert a dictionary of lists so list values become keys."""
    return dict( (v,k) for k in d for v in d[k] )
