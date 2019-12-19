from abc import ABC, abstractmethod

class Feature(ABC):

    def avg(self, l):
        return sum(l) / float(len(l))

    def get_weights(self, g):
        weights = [e['weight'] for e in g.es]
        if len(weights) == 0:
            weights = None

    @abstractmethod
    def compute(self, g, vertex_id):
        pass

    # self.extract_R_node_features, self.extract_R_graph_features,
