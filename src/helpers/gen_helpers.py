import logging

logger = logging.getLogger(__name__)

def invert_dict(d):
    """Function to invert a dictionary of lists so list values become keys."""
    return dict( (v,k) for k in d for v in d[k] )
