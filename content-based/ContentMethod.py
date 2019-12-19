import csv
import json
from Features.Feature import *


def fixed_split(train_file, test_file, annotations_file, filepath):
    """Loads messages from train and test splits and their annotations.

        Args:
         train_file: CSV file with rev_id of all messages to use in train split.
         test_file: CSV file with rev_id of all messages to use in test split.
         annotations_file: CSV file with columns 'rev_id' and 'annotation' for all annotated messages.
         filepath: Path to the directory containing all the conversation files.

        Returns:
         train, test: 2 dictionnaries with the annotations of messages in train and test indexed by their rev_id.
         comments: Dictionnary mapping comments (text) to rev_id.

    """
    train = {}
    with open(train_file, mode='r') as file:
        train_reader = csv.DictReader(file)
        for row in train_reader:
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
    file.close()

    comments = {}
    files = []
    for rev_id in train:
        files.append(filepath+"/%s_conversation.txt" % rev_id)
    for rev_id in test:
        files.append(filepath+"/%s_conversation.txt" % rev_id)

    for file in files:
        rev_id = file.split("/")[-1].replace("_conversation.txt", "")
        for line in open(file, 'r'):
            message = json.loads(line)
            if message["rev_id"] == rev_id:
                comments[rev_id] = message['cleaned_content']
                break


    return train, test, comments

def compute_features(train, test, comments, feature_list_file):
    """Computes all features.

        Args:
         train: Dictionnary with the annotations of messages in train split indexed by their rev_id.
         test: Dictionnary with the annotations of messages in test split indexed by their rev_id.
         comments: Dictionnary mapping comments (text) to rev_id.
         feature_list_file: File containing the name of all features to compute.

        Returns:
         

    """
    #list of tuples (rev_id, [features], [features_temporary], comment, annotation)
    train_feat = []
    for rev_id in train:
        train_feat.append((rev_id, [], {}, comments[rev_id], train[rev_id]))
    test_feat = []
    for rev_id in test:
        test_feat.append((rev_id, [], {}, comments[rev_id], test[rev_id]))

    feature_list = open(feature_list_file, "r")
    for feature in feature_list:
        feature = feature.replace("\n", "")
        c = globals()[feature]()
        c.compute(train_feat, test_feat)
    feature_list.close()

    #creates list of tuples (rev_id, [features], annotation)
    train_features = []
    for message in train_feat:
        train_features.append((message[0], message[1], message[4])) 
    test_features = []
    for message in test_feat:
        test_features.append((message[0], message[1], message[4])) 

    return train_features, test_features
