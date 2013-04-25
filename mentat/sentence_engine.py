from ConceptNetNode import *
from graph_search import *
import itertools as it
import sys
import string


def generate_stopword_list(stopwords):
    with open(stopwords) as f:
        words = f.readlines()
    stoplist = map(lambda s: s.strip(), words)
    return stoplist


def read_sentences_from_file(sentence_file):
    with open(sentence_file) as f:
        lines = f.readlines()
    clean_lines = map(lambda s: s.strip(), lines)
    return clean_lines


def generate_score_table():
    nodes = read_sentences_from_file(sys.argv[1])
    '''
    counter = 0
    for i in xrange(len(sentences)):
        #print "****************** \n"
        #print sentences[counter]
        #print sentences[counter+1]
        score = compare_sentences(sentences[counter], sentences[counter+1])
        print score
        #print "*************************** \n"
        counter += 3
    '''
    score = 0
    counter = 0
    for node_pair in nodes:
        node_pair = node_pair.translate(string.maketrans("", ""), string.punctuation)
        node_pair = node_pair.split()
        if node_pair != []:
            score += compare_nodes(node_pair[0], node_pair[1])
            counter += 1
        if node_pair == []:
            real_score = score / counter
            print real_score
            score = 0
            counter = 0


def compare_nodes(node1, node2):
    try:
        score = get_similarity_score(node1, node2)
    except:
        score = 0
    return score


def compare_sentences(sentence1, sentence2):
    node_list1, node_list2 = create_node_list(sentence1, sentence2)
    scores = []
    # generate permutations of nodes in list
    for pair in it.product(node_list1, node_list2):
        try:
            scores.append(get_similarity_score(pair[0], pair[1]))
        except:
            scores.append(0.0)
    return (sum(scores) / (len(node_list1) * len(node_list2)))



# gotta find a proper threshold, probably empirically
def create_node_list(sentence1, sentence2, threshold=1.4):
    node_list1 = []
    node_list2 = []
    sentence1 = sentence1.translate(string.maketrans("", ""), string.punctuation)
    sentence2 = sentence2.translate(string.maketrans("", ""), string.punctuation)
    #average_rank1 = sum([node_rank(word) for word in sentence1.split()]) / len(sentence1)
    #average_rank2 = sum([node_rank(word) for word in sentence2.split()]) / len(sentence2)
    sentence1_ranks = map(lambda x: node_rank(x), sentence1.split())
    sentence2_ranks = map(lambda x: node_rank(x), sentence2.split())
    avg_rank1 = sum(sentence1_ranks) / len(sentence1)
    avg_rank2 = sum(sentence2_ranks) / len(sentence2)
    STOPWORDS = generate_stopword_list('stopwords.txt')

    index = 0
    for word in sentence1.split():
        word = word.lower()
        if word not in STOPWORDS:
            if (sentence1_ranks[index] / avg_rank1) >= threshold:
                node_list1.append(word)
        index += 1
    index = 0
    for word in sentence2.split():
        word = word.lower()
        if word not in STOPWORDS:
            if (sentence2_ranks[index] / avg_rank2) >= threshold:
                node_list2.append(word)
        index += 1

    return node_list1, node_list2


if __name__ == "__main__":
    generate_score_table()
