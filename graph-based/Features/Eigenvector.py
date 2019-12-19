from Features.Feature import *

class eigen_c_w0_d0(Feature):
    def compute(self, d, vertex_id):
        val = g.eigenvector_centrality(directed=False)
        return [val[vertex_id], self.avg(val)]
                

class eigen_c_w0_d1(Feature):
    def compute(self, d, vertex_id):
        try:
            val = g.eigenvector_centrality(directed=True)
        except:
            return [0.0, 0.0]
        else:
            return [val[vertex_id], self.avg(val)]
                

class eigen_c_w1_d0(Feature):
    def compute(self, d, vertex_id):
        weights = self.get_weights(g)
        val = g.eigenvector_centrality(weights=weights, directed=False)
        return [val[vertex_id], self.avg(val)]
                

class eigen_c_w1_d1(Feature):
    def compute(self, d, vertex_id):
        weights = self.get_weights(g)
        try:
            val = g.eigenvector_centrality(weights=weights, directed=True)
        except:
            return [0.0, 0.0]
        else:
            return [val[vertex_id], self.avg(val)]
                