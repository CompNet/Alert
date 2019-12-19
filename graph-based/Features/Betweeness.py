from Features.Feature import *

class be_c_w0_d0(Feature):
    def compute(self, train_corpus, test_corpus, feature_name):
        val = g.betweenness(directed=False)
        return [val[vertex_id], self.avg(val)]

class be_c_w0_d1(Feature):
    def compute(self, train_corpus, test_corpus, feature_name):
        val = g.betweenness(directed=True)
        return [val[vertex_id], self.avg(val)]


class be_c_w1_d0(Feature):
    def compute(self, train_corpus, test_corpus, feature_name):
        weights = self.get_weights(g)
        val = g.betweenness(weights=weights, directed=False)
        return [val[vertex_id], self.avg(val)]

class be_c_w1_d1(Feature):
    def compute(self, train_corpus, test_corpus, feature_name):
        weights = self.get_weights(g)
        val = g.betweenness(weights=weights, directed=False)
        return [val[vertex_id], self.avg(val)]