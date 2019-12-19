import argparse as ap
import pickle
from ContentMethod import *
from Classifier import *
from Metrics import *

if __name__ == '__main__':
    p = ap.ArgumentParser()
    p.add_argument("-a", "--annotations", help="File containing the annotations for all messages. File generated using transform_annotation_file.py", type = str)
    p.add_argument("-md", "--messagesdir", help="Directory containing all conversation files (rev_id_conversation.txt files from figshare)", type = str)
    p.add_argument("-train", help="File containing Ids of all messages in train split", type = str)
    p.add_argument("-test", help="File containing Ids of all messages in test split", type = str)
    p.add_argument("-clf", "--classifier", help="Type of classifier to use", type = str, default="svm")
    p.add_argument("-f", "--features", help="File containing the subset of features to use", type = str)
    args = p.parse_args()

    #Load data
    #Obtain dict associating rev_id to the annotation of each messages in train and test splits
    train, test, comments = fixed_split(args.train, args.test, args.annotations, args.messagesdir)
    #Compute features
    train_feat, test_feat = compute_features(train, test, comments, args.features)

    '''
    save = open("train.pkl", 'wb') 
    pickle.dump(train_feat, save)
    save.close()
    save = open("test.pkl", 'wb') 
    pickle.dump(test_feat, save)
    save.close()
    with open("test.pkl", 'rb') as file:
        test_feat = pickle.load(file)
    file.close()
    with open("train.pkl", 'rb') as file:
        train_feat = pickle.load(file)
    file.close()
    '''

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