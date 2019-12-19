import csv
import random
import sys
import igraph

from compute_features import compute_features

csv.field_size_limit(sys.maxsize)


def fixed_split(train_file, test_file, annotations_file):
    """Loads messages from train and test splits and their annotations.

        Args:
         train_file: CSV file with rev_id of all messages to use in train split.
         test_file: CSV file with rev_id of all messages to use in test split.
         annotations_file: CSV file with columns 'rev_id' and 'annotation' for all annotated messages.

        Returns:
         2 dictionnaries with the annotations of messages in train and test indexed by their rev_id.
    """
    train = {}
    with open(train_file, mode='r') as file:
        train_reader = csv.DictReader(file)
        for row in train_reader:
            print (row)
            train[row['rev_id']] = None
    file.close()
    test = {}
    with open(test_file, mode='r') as file:
        test_reader = csv.DictReader(file)
        for row in test_reader:
            test[row['rev_id']] = None
    file.close()

    with open(annotations_file, mode='r') as file:
        annotations_reader = csv.DictReader(file)
        for row in annotations_reader:
            if row['rev_id'] in train:
                train[row['rev_id']] = row['annotation']
            elif row['rev_id'] in test:
                test[row['rev_id']] = row['annotation']
            else:
                print ("SPLIT ERROR")
    file.close()
    return train, test


def compute_feat(corpus, filepath, directed, window_size):
    """Computes the features for messages in corpus.

        Args:
         corpus: Dictionnary associating rev_id to annotation for all the messages to process.
         filepath: Path to the directory containing all the conversation files.
         directed: Boolean to indicate wheter to use directed or undirected graphs.
         window_size: Size of the window used to update the weights in the graph.

        Returns:
         A list of tuples with 1 tuple (rev_id, [features], annotation) for each message in corpus.
    """
    ret = []
    i = 0
    for rev_id in corpus:
        i += 1
        print ("%s/%s" % (i, len(corpus)))
        annotation = corpus[rev_id]

        # construct the conversation
        conv = []
        with open(filepath+"%s.csv" % rev_id, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for message in reader:
                #message [rev_id, timestamp, author, comment]
                conv.append(message)
                if len(message) > 0 and message[0] == rev_id:
                    annotated_message_index = len(conv)
        file.close()
        # create the pre and post conversations
        pre_conv = conv[:annotated_message_index]
        post_conv = conv[annotated_message_index-1:]
        full_conv = conv
        # build the 3 graphs
        pre_graph, pre_annotated_vertex_id = build_graph(rev_id, directed, window_size, pre_conv)
        post_graph, post_annotated_vertex_id = build_graph(rev_id, directed, window_size, post_conv)
        full_graph, full_annotated_vertex_id = build_graph(rev_id, directed, window_size, full_conv)
        # compute features based on the 3 graphs generated
        features = compute_features(full_graph, pre_graph, post_graph, full_annotated_vertex_id, pre_annotated_vertex_id, post_annotated_vertex_id)
        # append a tuple (rev_id, [features], annotation) to the result
        ret.append((rev_id, features, annotation))

    return ret

def get_targets(conversation, message_author):
    """Returns a list of users by how recent their last message is in the conversation

        Args:
         conversation: list of the last X messages in the conversation (X = window size).
         message_author: id of the author of the targeted message.

        Returns:
         List of users ID by how recent their last message.
    """
    #m[2] = message_author
    targets = []
    for m in conversation[::-1]:
        if m[2] not in targets and m[2] != message_author:
            targets.append(m[2])
    return targets

def get_weigths(targets):
    """Compute the weights of the edges. 

        Args:
         targets: List of users ID by how recent their last message.

        Returns:
         List of tuples (user_id, weight).
    """
    weigths = distrib_spread(len(targets))
    return [(targets[i], weigths[i]) for i in range(len(weigths))]

def distrib_spread(n, a = 1.0, r = .4):
    """Recursive method to compute the weight of all edges. The first receiver gets 60% of the total weight, 
    and the rest of them share the remaining 40% using the same recursive 60–40% split scheme.

        Args:
         n: Number of iteration remaining.
         a, r

        Returns:
         List of weights.
    """
    if n == 0:
        return []
    if n == 1:
        return [a]
    if n == 2:
        return [a * ( 1 - r ) , a * r]
    return [a * (1-r)] + distrib_spread(n-1, a*r, r)

def build_graph(rev_id, directed, window_size, conv):
    """Builds the conversational graph.

        Args:
         rev_id: id of the annotated message.
         directed: boolean
         window_size: Maximum number of messages to consider in the weight and edge update.
         conv: List of messages (conversation)

        Returns:
         The constructed graph and the id of the vertex corresponding to the author of the targeted author.
    """
    g = igraph.Graph(directed=directed)
    g['vnames'] = set()
    #we consider that a message replies only to the previous messages in the same sub-conversation (branch).
    current_branch = []

    #message [rev_id, timestamp, author, comment]
    #branchs are separated by empty line in the file
    for message in conv:
        #if this is en empty line, we start a new branch
        if len(message) == 0:
            current_branch = []
        #if this is not an empty line, the message is still in the same branch as the previous message.
        else:
            if message[0] == rev_id:
                annotated_message = message

            current_branch.append(message)
            # Check if message author in the graph, else add him.
            message_author = message[2]
            if message_author not in g['vnames']:
                g.add_vertex(name=str(message_author))
                g['vnames'].add(message_author)
            target_vertex = g.vs.find(name=str(message_author))
            #compute weights for the most recent messages in the current branch with a maximum of X messages (X = window_size).
            weights = get_weigths(get_targets(current_branch[-window_size:], message_author))
            for targeted_author, weight in weights:
                #retrieve the vertex corresponding to the targeted author
                v_targeted_author = g.vs.find(name=str(targeted_author))
                #retrieve the edge between author of the annotated message -> targeted_author
                edge_id = g.get_eid(target_vertex, v_targeted_author, directed=directed, error=False)
                if edge_id == -1: # edge does not exist
                    g.add_edges([(target_vertex, v_targeted_author)])    # add it
                    edge_id = g.get_eid(target_vertex, v_targeted_author, directed=directed, error=False)
                    g.es[edge_id]["weight"] = weight # and specify the weight
                else:
                    g.es[edge_id]["weight"] += weight
          
    #retrieve the id of the author of the annotated message
    targeted_vertex_id = g.vs.select(name=str(int(annotated_message[2])))[0].index

    return g, targeted_vertex_id
