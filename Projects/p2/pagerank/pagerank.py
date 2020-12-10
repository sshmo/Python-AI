import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
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
    
    # corpus should not be empty
    if len(corpus) == 0:
        raise "corpus should not be empty"
    
    # initialize the probability distribution dictionary
    prob = {}
    # sum_prob = 0
    
    # the given page has no links:
    if len(corpus[page]) == 0:
        for page_i in corpus:
            prob[page_i] = 1 / len(corpus)
            # sum_prob = sum_prob + prob[page_i]
    
    # the given page has liks to other pages
    else:
        for page_i in corpus:
            
            # page_i was linked via the given page
            if page_i in corpus[page]:
                prob[page_i] = (1 - damping_factor)/len(corpus) + damping_factor/len(corpus[page])
                # sum_prob = sum_prob + prob[page_i] 
            
            # page_i was not linked via the given page
            else:
                prob[page_i] = (1 - damping_factor)/len(corpus)
                # sum_prob = sum_prob + prob[page_i]  

    # print(sum_prob)
    return prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initializing a list of all pages
    pages = []

    # Initializing pagerank
    pagerank = {}

    for page_i in corpus:
        # Making a list of all pages to randomly pick one of them
        pages.append(page_i)
        # Initializeing each page probability
        pagerank[page_i] = 0

    # Pick a random page from pages
    page = pages[random.randrange(0, len(pages))]

    # Given the transition_model, pick sample pages from a previous page (n times)
    for _1 in range(n):

        prob = transition_model(corpus, page, damping_factor)
        
        # Making the population and weights for random.choice
        population = []
        weights = []
        for page, probaility in prob.items():
            population.append(page)
            weights.append(probaility)
        
        # Pick a weighted random page from pages
        page = random.choices(population, weights)[0]

        # Update the probability fot the picked page
        pagerank[page] += 1
    
    # Normalizing the results
    for pag_i in corpus:
        pagerank[pag_i] = pagerank[pag_i]/n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initializing pagerank and  each page rank probability
    pagerank = {}
    for page_i in corpus:
        pagerank[page_i] = 1 / len(corpus)
    
    # Initializing eps and tresh
    tresh = 0.002
    eps = 0.001

    while tresh > eps:
        
        # Initializing deltas: delta is the defrence between current pagerank[page_i] 
        # and previously calculated pagerank[page_i] 
        
        deltas = []
        sum_pagerank = 0
        
        for page_i in corpus:
            
            temp = pagerank[page_i]
            
            # Calculating pagerank[page_i] from pagerank formula
            sigma = 0
            for page_j in corpus:
                if corpus[page_j] == 0:
                    sigma += 1 / len(corpus)
                if page_i in corpus[page_j]:
                    sigma += pagerank[page_j]/len(corpus[page_j])
            pagerank[page_i] = (1 - damping_factor)/len(corpus) + damping_factor*sigma
            
            sum_pagerank += pagerank[page_i]
        
            # Updating deltas for page_i
            deltas.append(abs(pagerank[page_i]-temp))
        
        tresh = max(deltas)

    # Normalizing the results
    for page_i in corpus:
        pagerank[page_i] = pagerank[page_i]/sum_pagerank

    return pagerank


if __name__ == "__main__":
    main()
