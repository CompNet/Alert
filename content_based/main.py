import argparse as ap
from Alert import *
from Classifier import *
from Metrics import *

if __name__ == '__main__':
    p = ap.ArgumentParser()
    p.add_argument("-g", "--groundtruth", help="File containing the labels for all messages.", type = str)
    p.add_argument("-md", "--messagesdir", help="Directory containing all conversation files.", type = str)
    p.add_argument("-vm", "--validation-method", choices=["basic", "cv"], help="Validation method to use: basic or cross validation", type = str, default = 'basic')
    p.add_argument("-train", help="File containing Ids of all messages in train split", type = str)
    p.add_argument("-test", help="File containing Ids of all messages in test split", type = str)
    p.add_argument("-cvnb", "--cv-number", help="Number of folds to use in the cross validation", type = int)
    p.add_argument("-r", "--traintest-repartition", help="Percentage of folds to use in the test subset", type = int, default = 30)
    p.add_argument("-f", "--features", help="File containing the subset of features to use", type = str, default="features.txt")
    p.add_argument("-c", "--classifier", help="Type of classifier to use", type = str, default="svm")
    args = p.parse_args()

    #Create system
    if args.validation_method == "basic":
        a = AlertBasic(args.traintest_repartition)
    elif args.validation_method == "cv":
        a = AlertCrossValidation(args.cv_number, args.traintest_repartition)

    #Load data
    messages = a.load_data(args.groundtruth, args.messagesdir)

    #Split data
    if args.train is not None and args.test is not None:
        a.fixed_split(messages, args.train, args.test)
    else:
        a.random_split(messages)

    #Compute features
    a.compute_features(args.features)

    # Train classifier
    if args.classifier == "svm":
        clf = SVMClassifier()
    a.train(clf)

    # Test classifier
    a.test()
    a.evaluate(F1Evaluator())