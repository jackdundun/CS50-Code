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

    trans_model = {}
    rand_choice = random.choices(('main', 'chance'), weights=[damping_factor, 1 - damping_factor])

    num_pages = len(corpus)
    num_links = len(corpus.get(page))

    page_prob = ((1 - damping_factor) / num_pages)
    if num_links > 0:
        link_prob = ( (damping_factor / num_links) + page_prob )

    equal_prob = 1/num_pages

    if (rand_choice == ['chance']) or (num_links == 0):
        for page in corpus:
            trans_model[page] = equal_prob
        return trans_model
    else:
        trans_model[page] = page_prob
        keys = corpus[page]
        for key in keys:
            trans_model[key] = link_prob
        return trans_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #choosing a random page
    start_page = random.choice(list(corpus.keys()))

    #creating the dict to return
    sample_dict = {}
    for page in corpus:
        sample_dict.update({page: 0})

    #def transition_model(corpus, page, damping_factor):

    trans_mod = transition_model(corpus, start_page, damping_factor)

    next_page = random.choices(list(trans_mod.keys()), weights=list((trans_mod.values())))
    next_page = next_page[0]
    sample_dict[next_page] += 1

    for i in range(n-1):
        trans_mod = transition_model(corpus, next_page, damping_factor)
        next_page = random.choices(list(trans_mod.keys()), weights=list(trans_mod.values()))
        next_page = next_page[0]
        sample_dict[next_page] += 1

    #dividing the values by the samples
    sample_dict = {k: v / SAMPLES for k, v in sample_dict.items()}
    print(sum(sample_dict.values()))
    return sample_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # number of pages
    num_pages = len(corpus)

    it_dict = {}
    for page in corpus:
        it_dict.update({page: 1/num_pages})

    #calculating new values based on old
    iterate = True
    counter = 1
    for key in corpus:
        if len(corpus.get(key)) == 0:
            corpus[key] = set(corpus.keys())
    while iterate:
        it_dict_copy = it_dict.copy()
        dict_for_transfers = {}
        for key in it_dict:
            marker = False
            summer = 0
            for dif_key in corpus:
                if key != dif_key:
                    if key in corpus[dif_key]:
                        marker = True
                        summer += it_dict[dif_key] / len(corpus[dif_key])
            if marker == True:
                dict_for_transfers[key] = ((1 - damping_factor) / num_pages) + (damping_factor * summer)

        for key in it_dict:
            if key in dict_for_transfers:
                it_dict[key] = dict_for_transfers[key]
            else:
                it_dict[key] = (1 - damping_factor) / num_pages
        counter += 1
        tester = 0

        for key in it_dict:
            if abs(it_dict[key] - it_dict_copy[key]) < 0.001:
                tester += 1
        if tester == num_pages:
            iterate = False

    return it_dict

if __name__ == "__main__":
    main()
