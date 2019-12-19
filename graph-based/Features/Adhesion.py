from Features.Feature import *
      
class adhesion(Feature):

    def compute(self, g, vertex_id):
        val = g.adhesion()
        return val