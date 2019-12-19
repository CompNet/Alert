from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np

#

class SVMClassifier():

    def fit(self, train):
        """Trains the model

        Args:
         train: List of tuples (rev_id, [features], annotation).
        """
        features_train = []
        annotations_train = []
        for rev_id,features,annotation in train:
            features_train.append(features)
            annotations_train.append(int(annotation))

        self.scaler = StandardScaler().fit(features_train)
        features_train_scaled = self.scaler.transform(features_train)

        self.classifier = SVC(class_weight='balanced', probability=True)
        self.classifier.fit(features_train_scaled, annotations_train)

    def predict(self, test):
        """Classification.

        Args:
         test: List of tuples (rev_id, [features], annotation).
        """
        features_test = []
        annotations_test = []
        for rev_id,features,annotation in test:
            features_test.append(features)
            annotations_test.append(int(annotation))
        #use the same scaler as for the training
        features_test_scaled = self.scaler.transform(features_test)

        #predictions are stored in the classifier object
        self.predictions = self.classifier.predict(features_test_scaled)
        predictions_proba = self.classifier.predict_proba(features_test_scaled)
        self.predictions_p = [p[1] for p in predictions_proba]
        self.Y_true = annotations_test

