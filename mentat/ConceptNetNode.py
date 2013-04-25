from __future__ import unicode_literals
import urllib2
import json


class ConceptNetNode(object):
    '''
    This is a wrapper object for Conceptnet DB results that makes it easier to work with in terms of graph search. 
    The following are fields from the JSON result that are then converted in Python object attributes by way of
    self.create_attrs_from_response()
    
    id: the unique ID for this edge, which contains a SHA-1 hash of the information that makes it unique.
    uri: the URI of the assertion being expressed. The uri is not necessarily unique, because many edges can bundle together to express the same assertion.
    rel: the URI of the predicate (relation) of this assertion.
    start: the URI of the first argument of the assertion.
    end: the URI of the second argument of the assertion.
    weight: the strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher, lower, or even negative.
    sources: the sources that, when combined, say that this assertion should be true (or not true, if the weight is negative).
    license: a URI representing the Creative Commons license that governs this data. See Copying and sharing ConceptNet.
    dataset: a URI representing the dataset, or the batch of data from a particular source that created this edge.
    context: the URI of the context in which this statement is said to be true.
    features: a list of three identifiers for features, which are essentially assertions with one of their three components missing.
    surfaceText: the original natural language text that expressed this statement. '''

    def __init__(self, node_name, request=None, convert=False, prox_score=0, degree='', rows=100):
        self.node_name = node_name
        self.score = prox_score
        self.edges = []
        #converted
        self.cnet_edges = {}
        #print node_name

        if request != None:
            self.cnet_response = self.search_solr(request)
        else:
            self.cnet_response = self.search_solr(self.build_request(self.node_name, rows=rows))

        if self.cnet_response != {}:
            self.edges = self.create_adjacency_list(self.cnet_response, degree=degree)
            self.create_attrs_from_response(self.cnet_response)
        if convert:
            self.convert_list_to_nodes()

        self.edges = set(self.edges)

    def __repr__(self):
        return self.node_name

    def create_attrs_from_response(self, response):
        try:
            for key, value in response['response']['docs'][0].iteritems():
                setattr(self, key, value)
        except:
            pass

    def build_request(self, node_name, rows=50, format="json"):
        formatted_name = node_name.replace('_', '+')
        formatted_name = '"' + formatted_name + '"'
        formatted_name = self._escape_name(formatted_name)
        request = u"http://localhost:8983/solr/select/?q=startLemmaString:{0}&version=2.2&start=0&rows={1}&indent=on&wt={2}".format(formatted_name, rows, format)
        return request

    def _escape_name(self, name):
        try:
            start = name.index('&')
            name = name[:start] + "%26" + name[start + 1:]
        except:
            pass
        return name

    def create_adjacency_list(self, cnet_response, degree=''):
        adjacent_nodes = []
        if degree == '':
            key = 'endLemmaString'
        else:
            key = degree
        for entry in cnet_response['response']['docs']:
            adjacent_nodes.append(entry[key])
        return adjacent_nodes

    def convert_list_to_nodes(self):
        for lemma in self.edges:
            search_term = lemma.replace(' ', '_')
            value = ConceptNetNode(search_term)
            self.cnet_edges[lemma] = value

    def search_solr(self, request_string):
        req = urllib2.Request(request_string)
        opener = urllib2.build_opener()
        json_result = {}
        try:
            f = opener.open(req)
            json_result = json.loads(f.read())
        except:
            pass
        return json_result
