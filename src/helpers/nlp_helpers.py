import logging

logger = logging.getLogger(__name__)

def word2ngrams(text, n=4, exact=True):
    """Convert text into ngrams."""
    return ["".join(g) for g in zip(*[text[i:] for i in range(n)])]

def sim4gram(text1, text2):
    """Calculate ngram similarity metric."""
    list1 = word2ngrams(text1)
    list2 = word2ngrams(text2)
    return len(list(set(list1) & set(list2)))/len(list(set(list1) | set(list2)))
