from Features.Feature import *

class com_modularity_w0(Feature):
    def compute(self, g, vertex_id):
        vertexcluster = g.community_infomap()
        return vertexcluster.modularity

class com_nCom_w0(Feature):
    def compute(self, g, vertex_id):
        vertexcluster = g.community_infomap()
        clustergraph = vertexcluster.cluster_graph()
        return len(clustergraph.vs)

class com_modularity_w1(Feature):
    def compute(self, g, vertex_id):        
        weights = self.get_weights(g)
        vertexcluster = g.community_infomap(edge_weights=weights)
        return vertexcluster.modularity

class com_nCom_w1(Feature):
    def compute(self, g, vertex_id):      
        weights = self.get_weights(g)
        vertexcluster = g.community_infomap(edge_weights=weights)
        clustergraph = vertexcluster.cluster_graph()
        return len(clustergraph.vs)