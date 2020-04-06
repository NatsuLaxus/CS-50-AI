import os
import random
import re
import sys
# import pomegranate  
from pomegranate import *
# import random

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus0")
    corpus = crawl(sys.argv[1])
    # print("r")
    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # my_code
    # linked_pages = []
    # linked_pages = list(corpus[page])
    # numlinks = len(linked_pages)
    # if numlinks == 0:
    #     damping_factor = 0
    # total = len(corpus)
    # prob1 = numlinks/total
    # prob_dis = {}
    # for c in corpus:
    #     prob_dis[c] = 0
    #     if c in linked_pages:
    #         prob_dis[c] = prob1*damping_factor
    #     prob_dis[c] = prob_dis[c] + ((1-damping_factor)*(1/total))
    # return prob_dis
    # pages = corpus.keys()
    # distribution = dict()
    

    #siddhant's code
    for p in pages:
        distribution[p] = (1-damping_factor)/len(pages)

    direct = list(corpus[page])

    if len(direct) == 0:
        direct = pages

    for p in direct:
        distribution[p] += damping_factor/len(direct)

    return distribution
    # raise NotImplementedError

def sample_pagerank(corpus, damping_factor, n):
    pages = []
    weights = []
    corpus_keys = list(corpus.keys())
    s = len(corpus_keys)
    c = corpus_keys[random.randrange(s)]

    count = {}
    count[c] = 1
    for c in corpus_keys:
        count[c] = 0
    state = {}
    for i in range(1,n):
        transitionModel = transition_model(corpus, c, damping_factor)
        pages = transitionModel.keys()
        weights = transitionModel.values()
        website = Node(DiscreteDistribution(transitionModel), name="website")
        model = BayesianNetwork()
        model.add_states(website)
        model.bake()
        for state in model.states:
            c = state.distribution.sample()
            count[c] = count[c]+1

    for c in corpus_keys:
        count[c] = count[c]/n
    return count

def iterate_pagerank(corpus, damping_factor):
    corpus_keys = list(corpus.keys())
    newpr = {}
    pr = {}
    n = len(corpus_keys)
    for c in corpus_keys:
        pr[c] = 1/n
    numlinks = {}
    for num in corpus:
        if len(corpus[num]) == 0:
            numlinks[num] = n
        else:
            numlinks[num] = len(corpus[num])
    diff = True
    while diff:
        newpr = 0
        for c in corpus_keys:
            newpr = (1-damping_factor)/n
            for i in corpus[c]:
                newpr = newpr + damping_factor*(pr[i]/numlinks[i])
            if((newpr-pr[c])<0.0001):
                diff = False
            pr[c] = newpr
    return pr

if __name__ == "__main__":
    main()
