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

# Test for word2grams.
seed_word = 'foobarbarblacksheep'
word2ngram_result = ['foo', 'oob', 'oba', 'bar', 'arb', 'rba', 'bar', 'arb', 'rbl', 'bla',
'lac', 'ack', 'cks', 'ksh', 'she', 'hee', 'eep']

text1 = 'black'
text2 = 'redsheep'
list1 = word2ngrams(text1)
list2 = word2ngrams(text2)
test_result = len(list(set(list1) & set(list2)))/len(list(set(list1) | set(list2)))

# Test to see if 3 grams were created correctly.
def test_word2gram():
    assert(word2ngrams(seed_word, n=3) == word2ngram_result)

# Test to see if similarity sscore was calculated correctly.
def test_sim2gram():
    assert(sim4gram(text1, text2) == test_result)
