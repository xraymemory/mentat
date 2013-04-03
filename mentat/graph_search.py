#from scipy.special import *
from ConceptNetNode import *
#from graph_search import ConceptNetNode

BASE_PROXIMITY = 2000
RETAIN_AMOUNT = 0.8


def get_similarity_score(start, end, max_path=3):
    path = bfs(start, end, max_path=max_path)
    edge_weights = 0.0
    edge_prox = 0.0
    if len(path) == 1:
        return 1
    for node in path:
        edge_weights += node.weight ** (1 / 2.0)
        edge_prox += node.score
    edge_prox = edge_prox / BASE_PROXIMITY
    similarity_score = edge_weights / ((len(path) ** 2) - edge_prox)
    return similarity_score


def get_sim_score_2(start, end, max_path=3):
    ''' wthout prox score'''
    path = bfs(start, end, max_path=max_path)
    edge_weights = 0.0
    for node in path:
        edge_weights += node.weight ** (1 / 2.0)
    similarity_score = edge_weights / ((len(path) ** 2))
    return similarity_score


def bfs(start, end, max_path=3):
    start_node = ConceptNetNode(start, convert=True)
    end_node = ConceptNetNode(end, convert=True)
    visited = []
    queue = []
    queue.append([start_node])

    start_node.score = _inject_initial_proximity(start_node)

    if start == end:
        return [start_node]

    if end_node.startLemmaString in start_node.cnet_edges:
        end_node.score = (start_node.score / len(start_node.edges)) * RETAIN_AMOUNT
        return [start_node, end_node]

    while queue:
        path = queue.pop(0)
        if len(path) > max_path:
            return []
        node = path[-1]
        try:
            relative_proximity = node.score / len(node.edges)
        except ZeroDivisionError:
            relative_proximity = node.score / 1

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
                new_node.score = relative_proximity * RETAIN_AMOUNT
                visited.append(new_node.node_name)
                new_node.convert_list_to_nodes()
                new_path.append(new_node)
                queue.append(new_path)


def node_rank(cnet_node, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
    nodes = list(cnet_node.edges)
    nodes.append(cnet_node.node_name)
    neighbor_count = len(nodes)
    min_value = (1.0 - damping_factor) / neighbor_count
    rank_dict = dict.fromkeys(nodes, 1.0 / neighbor_count)

    for i in xrange(max_iterations):
        diff = 0
        for node in nodes:
            activated_node = ConceptNetNode(node)
            rank = min_value
            for referring_node in activated_node.edges:
                if referring_node not in rank_dict:
                    rank_dict[referring_node] = 1.0 / neighbor_count
                rank += damping_factor * rank_dict[referring_node] / len(activated_node.edges)
            diff += abs(rank_dict[node] - rank)
            rank_dict[node] = rank

        if diff < min_delta:
            break

    return rank_dict


def _inject_initial_proximity(node):
    initial_prox_score = BASE_PROXIMITY
    node.score = initial_prox_score
    remaining_prox = initial_prox_score * RETAIN_AMOUNT
    return remaining_prox
