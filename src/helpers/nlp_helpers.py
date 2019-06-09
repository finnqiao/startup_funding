import logging

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)

def word2ngrams(text, n=4, exact=True):
    """Convert text into ngrams.
    Args:
        text (str): String to be parsed into ngrams
        n (int): Number of characters in each ngram
        exact (bool): Exact match
    Returns: List of potential ngrams of length n
    >>> word2ngrams('foobarbarblacksheep')
    ['foo', 'oob', 'oba', 'bar', 'arb', 'rba', 'bar', 'arb', 'rbl', 'bla',
    'lac', 'ack', 'cks', 'ksh', 'she', 'hee', 'eep']
    """
    return ["".join(g) for g in zip(*[text[i:] for i in range(n)])]

def sim4gram(text1, text2):
    """Calculate ngram similarity metric."""
    list1 = word2ngrams(text1)
    list2 = word2ngrams(text2)
    return len(list(set(list1) & set(list2)))/len(list(set(list1) | set(list2)))
