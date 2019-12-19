import argparse as ap
import datetime
import pickle
from GraphMethod import *
from Metrics import *
from Classifier import *


if __name__ == '__main__':
    p = ap.ArgumentParser()
    p.add_argument("-a", "--annotations", help="File containing the annotations for all messages. File generated using transform_annotation_file.py", type = str)
    p.add_argument("-md", "--messagesdir", help="Directory containing all conversation files. Conversations generated using transform_conversations.py", type = str)
    p.add_argument("-train", help="File containing Ids of all messages in train split", type = str)
    p.add_argument("-test", help="File containing Ids of all messages in test split", type = str)
    p.add_argument("-clf", "--classifier", help="Type of classifier to use", type = str, default="svm")
    p.add_argument("-w", "--window-size", help="Size of window used for the weight update", type = int, default = 10)
    p.add_argument("-d", "--directed", help="Type of graph to use (directed or not)", action="store_true")
    args = p.parse_args()

    #Split data
    #Obtain dict associating rev_id to the annotation of each messages in train and test splits
    train, test = fixed_split(args.train, args.test, args.annotations)

    #Compute features for train and test.
    #Obtain list of tuples (rev_id, [features], annotation)
    train_feat = compute_feat(train, args.messagesdir, directed = args.directed, window_size = args.window_size)
    test_feat = compute_feat(test, args.messagesdir, directed = args.directed, window_size = args.window_size)

    #save features
    save = open("train.pkl", 'wb') 
    pickle.dump(train_feat, save)
    save.close()
    save = open("test.pkl", 'wb') 
    pickle.dump(test_feat, save)
    save.close()
    #load previously computed features
    '''with open("test.pkl", 'rb') as file:
        test_feat = pickle.load(file)
    file.close()
    with open("train.pkl", 'rb') as file:
        train_feat = pickle.load(file)
    file.close()'''

    # Train classifier
    #it is possible to implement and use other classifiers
    if args.classifier == "svm":
        clf = SVMClassifier()
    clf.fit(train_feat)

    # Test 
    clf.predict(test_feat)

    # Performances
    metric = F1Evaluator()
    metric.evaluate(clf)
