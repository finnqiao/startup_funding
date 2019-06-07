import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

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
    df = pd.concat([df, pd.get_dummies(df[column], prefix=column)], axis=1)
    df = df.drop(column, axis=1)
    return df

def invert_dict(d):
    """Function to invert a dictionary of lists so list values become keys.
    Args:
        d (dict): Dictionary of lists
    Returns: Dictionary with list values expanded into keys and keys becoming values

    Example:
        >>> d = {1:[a,b], 2:[c,d]}
        >>> print(invert_dict(d))
        {a:1, b:1, c:2, d:2}
    """
    return dict( (v,k) for k in d for v in d[k] )
