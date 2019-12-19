from Features.Feature import *
      
class cohesion(Feature):

    def compute(self, g, vertex_id):
        val = g.cohesion()
        return val