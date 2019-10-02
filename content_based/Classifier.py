from abc import ABC, abstractmethod
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

class Classifier(ABC):

    @abstractmethod
    def fit(self, features_train, labels_train):
        pass

    @abstractmethod
    def predict(self, features_test, labels_test):
        pass


class SVMClassifier(Classifier):

    def fit(self, features_train, labels_train):
        self.scaler = StandardScaler().fit(features_train)
        features_train_scaled = self.scaler.transform(features_train)

        self.classifier = SVC(class_weight='balanced', probability=True)
        self.classifier.fit(features_train_scaled, labels_train)

    def predict(self, features_test, labels_test):
        features_test_scaled = self.scaler.transform(features_test)
        predictions = self.classifier.predict(features_test_scaled)
        predictions_proba = self.classifier.predict_proba(features_test_scaled)
        predictions_p = [p[1] for p in predictions_proba]
        return predictions, predictions_p