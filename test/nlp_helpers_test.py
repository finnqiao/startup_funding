import pytest
import pandas as pd
import pandas.util.testing as pdt
import os
import sys
import logging
sys.path.append(os.path.abspath('./src'))
from helpers.nlp_helpers import word2ngrams, sim4gram

logging.basicConfig(level=logging.DEBUG, filename="test_logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
