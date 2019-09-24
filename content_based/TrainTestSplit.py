import importlib
import csv
from Features.Feature import *
from sklearn.metrics import f1_score


class TrainTestSplit:

    def __init__(self):
        self.test = []
        self.train = []
        self.classifier = None
        
    def set_splits(self, train, test):
        """Set train and test splits.

        Args:
         train: List of messages in train split.
         test: List of messages in test split.
        """
        self.train = train
        self.test = test

    def compute_features(self, feature_list_file):
        #self.feature_extractor = FeatureExtractor.FeatureExtractor(feature_list)
        #self.feature_extractor.compute_features(self, feature_list)

        feature_list = open(feature_list_file, "r")
        for feature in feature_list:
            feature = feature.replace("\n", "")
            c = globals()[feature]()
            c.compute(self.train, self.test)
        feature_list.close()

    def train_model(self, model):
        self.classifier = model
        features_train = [message.getFeatures() for message in self.train]
        labels_train = [message.get_label() for message in self.train]
        self.classifier.fit(features_train, labels_train)

    def test_model(self):
        features_test = [message.getFeatures() for message in self.test]
        labels_test = [message.get_label() for message in self.test]
        self.true_labels = labels_test
        self.predictions = self.classifier.predict(features_test, labels_test)