from ConceptNetNode import *
from graph_search import *
from stopwords import STOPWORDS
import itertools as it
import sys


def read_sentences_from_file(sentence_file):
    with open(sentence_file) as f:
        lines = f.readlines()
    return lines


def generate_score_table():
    sentences = read_sentences_from_file(sys.argv[1])
    counter = 0
    for i in xrange(len(sentences)):
        print "****************** \n"
        print sentences[counter]
        print sentences[counter+1]
        score = compare_sentences(sentences[counter], sentences[counter+1])
        print score
        print "*************************** \n"
        counter += 2


def compare_sentences(sentence1, sentence2):
    node_list1, node_list2 = create_node_list(sentence1, sentence2)
    scores = []
    # generate permutations of nodes in list
    for pair in itertools.product(node_list1, node_list2):
        scores.append(get_similarity_score(pair[0], pair[1]))
    return sum(normalize_scores(scores))


def normalize_scores(scores, normalize_height=1):
    max_score = max(scores)
    return [score / (max_score * 1.0) * normalize_height for score in scores]


# gotta find a proper threshold, probably empirically
def create_node_list(sentence1, sentence2, threshold=0.5):
    node_list1 = []
    node_list2 = []
    average_rank1 = sum([graph_search.node_rank(word) for word in sentence1])
    average_rank2 = sum([graph_search.node_rank(word) for word in sentence2])

    for word in sentence1:
        if word not in STOPWORDS:
            if (graph_search.node_rank(word) / average_rank1) >= threshold:
                node_list1.append(word)
    for word in sentence2:
        if word not in STOPWORDS:
            if (graph_search.node_rank(word) / average_rank2) >= threshold:
                node_list2.append(word)

    return node_list1, node_list2
