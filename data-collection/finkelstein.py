import csv
import os
import sys

mentat_path = os.path.abspath('../mentat/')
sys.path.append(mentat_path)
from graph_search import get_similarity_score as get_scores
from graph_search import get_sim_score_2


input_file = sys.argv[1]


def _read_in_csv(input_file):
    with open(input_file, 'rb') as f:
        fink_csv = csv.reader(f)
        node1 = []
        node2 = []
        scores = []
        for row in fink_csv:
            node1.append(row[0])
            node2.append(row[1])
            scores.append(row[2])
    return (node1, node2, scores)


def _generate_cnet_scores(comparisons):
    node1 = comparisons[0]
    node2 = comparisons[1]
    fink_scores = comparisons[2]
    for index in range(len(fink_scores)):
        try:
            print get_scores(node1[index], node2[index])
        except:
            print -1
    print "-----WITHOUT PROX----- \n"
    for index in range(len(fink_scores)):
        try:
            print get_sim_score_2(node1[index], node2[index])
        except:
            print -1


def generate_data(input_fle=input_file):
    fink_tuple = _read_in_csv(input_file)
    _generate_cnet_scores(fink_tuple)


if __name__ == '__main__':
    generate_data()
