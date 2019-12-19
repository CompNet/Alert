from Features.Feature import *

class apl_d0(Feature):

    def compute(self, g, vertex_id):
        val = g.average_path_length(directed=False)
        return val
                
class apl_d1(Feature):

    def compute(self, g, vertex_id):
        val = g.average_path_length(directed=True)
        return val
