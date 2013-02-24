#from scipy.special import *
from ConceptNetNode import *
from graph_search import ConceptNetNode


def get_similarity_score(start, end):
    path = bfs(start, end)
    edge_score = 0.0
    for node in path:
        print "Node is " + str(node.node_name)
        print "Node weight is " + str(node.weight)
        edge_score += node.weight ** (1 / 3.0)
    similarity_score = edge_score / (len(path) ** 2)
    return similarity_score


def bfs(start, end):
    start_node = ConceptNetNode(start, convert=True)
    end_node = ConceptNetNode(end, convert=True)
    visited = []
    queue = []
    queue.append([start_node])

    if end_node.startLemmaString in start_node.cnet_edges:
        return [start_node, end_node]

    while queue:
        path = queue.pop(0)
        node = path[-1]
        try:
            matching_term = node.startLemmaString
        except AttributeError:
            matching_term = ""
        if matching_term in end_node.cnet_edges:
            return path
        for nodes in node.cnet_edges.iteritems():
            new_path = list(path)
            new_node = nodes[1]
            if new_node.node_name not in visited:
                visited.append(new_node.node_name)
                new_node.convert_list_to_nodes()
                new_path.append(new_node)
                queue.append(new_path)
