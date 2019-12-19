import importlib
import csv
from numpy import *
from Features.Feature import *
from Features.Eigenvector import *
from Features.Pagerank import *
from Features.Betweeness import *
from Features.Closeness import *
from Features.Eccentricity import *
from Features.Hub import *
from Features.Degree import *
from Features.AssortativityDegree import *
from Features.AuthorityScore import *
from Features.AveragePathLength import *
from Features.Coreness import *
from Features.Density import *
from Features.EdgeCount import *
from Features.VerticeCount import *
from Features.Strength import *
from Features.Transitivity import *
from Features.Diameter import *
from Features.Radius import *
from Features.Clusters import *
from Features.Community import *
from Features.Cohesion import *
from Features.Adhesion import *
from Features.Clique import *
from Features.R_node_features import *
from Features.R_graph_features import *
from sklearn.metrics import f1_score


 
def compute_features(g_full, g_before, g_after, targeted_id_full, targeted_id_before, targeted_id_after):
    """Computes all the features (153*3) for a specific message.

        Args:
         g_full: Graph with all messages.
         g_before: Graph with messages posted before the targeted message
         g_after: Graph with messages posted after the targeted message
         targeted_id_full: id of the targeted message's author in full graph.
         targeted_id_before: id of the targeted message's author in before graph.
         targeted_id_after: id of the targeted message's author in after graph.

        Return:
         List of 459 features (153 per graph). When a feature is not defined, default value is 0.

        """
    
    feature_no_avg = ["nV", "trans_loc_d0_w0", "trans_loc_d0_w1", "trans_avgloc_d0", "trans_d0",
    "radius_in", "radius_out", "radius_all", "nE", "diameter_d0_w0", "diameter_d0_w1", 
    "diameter_d1_w0", "diameter_d1_w1", "density", "com_modularity_w0", "com_nCom_w0",
    "com_modularity_w1", "com_nCom_w1", "cohesion", "cluster_strong", "cluster_weak", 
    "clique_number", "apl_d0", "apl_d1", "ad_d0", "ad_d1", "adhesion"]
    #Features computed + its average value
    features_avg = ["in_str_w0", "in_str_w1", "out_str_w0", "out_str_w1", "all_str_w0", 
    "all_str_w1", "pr_c_w0_d0", "pr_c_w0_d1", "pr_c_w1_d0", "pr_c_w1_d1", "hub_w0",
    "hub_w1", "eigen_c_w0_d0", "eigen_c_w0_d1", "eigen_c_w1_d0", "eigen_c_w1_d1", 
    "in_ecc", "out_ecc", "all_ecc", "in_deg", "out_deg", "all_deg", "in_core", "out_core",
    "all_core", "in_clo_w0", "in_clo_w1", "out_clo_w0", "out_clo_w1", "all_clo_w0", 
    "all_clo_w1", "be_c_w0_d0", "be_c_w0_d1", "be_c_w1_d0", "be_c_w1_d1", "as_w0", 
    "as_w1"]
    #features computed with R script
    r_graph = ["Reciprocity"]
    r_node = ["Alpha_Unweighted"]
    

    '''Sometimes, several features can't be computed because of the graph characteristics.
    In this case, the default value is 0.
    Features can be added in Features/
    '''
    #print ("**************FULL*************")
    features = []
    for funcname in feature_no_avg:
        c = globals()[funcname]()
        try:
            feat = c.compute(g_full, targeted_id_full)
            features.append(feat)
        except:
            features.append(0)

    for funcname in features_avg:
        c = globals()[funcname]()
        try:
            feat = c.compute(g_full, targeted_id_full)
            features.append(feat[0])
            features.append(feat[1])
        except:
            features.append(0.0)
            features.append(0.0)

    funcname = "Reciprocity"
    c = globals()[funcname]()
    try:
        feat = c.compute(g_full, targeted_id_full)
        for val in feat:
            features.append(feat[val])

    except:
        features.append(0.0)
        features.append(0.0)


    funcname = "Alpha_Unweighted"
    c = globals()[funcname]()
    try:
        feat = c.compute(g_full, targeted_id_full)
        for val in feat:
            features.append(feat[val])
    except:
        for i in range(50):
            features.append(0.0)
    
    ##############################""
    #print ("**************BEFORE*************")

    for funcname in feature_no_avg:
        c = globals()[funcname]()
        try:
            feat = c.compute(g_before, targeted_id_before)
            features.append(feat)
        except:
            features.append(0)

    for funcname in features_avg:
        c = globals()[funcname]()
        try:
            feat = c.compute(g_before, targeted_id_before)
            features.append(feat[0])
            features.append(feat[1])
        except:
            features.append(0.0)
            features.append(0.0)

    funcname = "Reciprocity"
    c = globals()[funcname]()
    try:
        feat = c.compute(g_before, targeted_id_before)
        for val in feat.values():
            features.append(val)
    except:
        features.append(0.0)
        features.append(0.0)

    funcname = "Alpha_Unweighted"
    c = globals()[funcname]()
    try:
        feat = c.compute(g_before, targeted_id_before)
        for val in feat.values():
            features.append(val)
    except:
        for i in range(50):
            features.append(0.0)
    

    ##############################""
    #print ("**************AFTER*************")

    for funcname in feature_no_avg:
        c = globals()[funcname]()
        try:
            feat = c.compute(g_after, targeted_id_after)
            features.append(feat)
        except:
            features.append(0)

    for funcname in features_avg:
        c = globals()[funcname]()
        try:
            feat = c.compute(g_after, targeted_id_after)
            features.append(feat[0])
            features.append(feat[1])
        except:
            features.append(0.0)
            features.append(0.0)

    funcname = "Reciprocity"
    c = globals()[funcname]()
    try:
        feat = c.compute(g_after, targeted_id_after)
        for val in feat.values():
            features.append(val)
    except:
        features.append(0.0)
        features.append(0.0)

    funcname = "Alpha_Unweighted"
    c = globals()[funcname]()
    try:
        feat = c.compute(g_after, targeted_id_after)
        for val in feat.values():
            features.append(val)
    except:
        for i in range(50):
            features.append(0.0)

    #replace undefined features by 0
    for i in range(len(features)):
        if isnan(features[i]):
            features[i] = 0.0
    return features
