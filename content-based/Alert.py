import csv
import glob
import random
import copy

from abc import ABC, abstractmethod
from TrainTestSplit import TrainTestSplit
from Message import Message, LabeledMessage


class Alert(ABC):

    @abstractmethod
    def fixed_split(self, corpus, train_file, test_file):
        pass

    @abstractmethod
    def random_split(self, corpus):
        pass

    @abstractmethod
    def save_split(self):
        pass

    @abstractmethod
    def compute_features(self, feature_list):
        pass

    @abstractmethod
    def train(self, model):
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def evaluate(self, metric):
        pass

    @staticmethod
    def load_message(conversation_id, message_id, message_dir):
        """Loads message from file based on it's ID and conversation ID.

        Args:
         conversation_id: Conversation in which the message appears.
         message_id: Message identifier.
         message_dir: Directory containing all conversation files.

        Returns:
         The corresponding labeled message.
        """
        with open("%s/%s.csv" % (message_dir, conversation_id), mode='r') as file:
            reader = csv.DictReader(file, fieldnames=("msg_id", "date", "author", "text"))
            for m in reader:
                if m['msg_id'] == message_id:
                    message = LabeledMessage(m['msg_id'], m['author'], m['date'], m['text'])
                    file.close()
                    return message

    def load_data(self, groundtruth_file, message_dir):
        """Loads data from file.

        Args:
          groundtruth_file: CSV file containing the ground truth.
          message_dir: Directory containing all conversation files.
        Returns:
          A list of all the messages.
        """
        messages = []
        with open(groundtruth_file, mode='r') as groundtruth:
            reader = csv.DictReader(groundtruth, fieldnames=("conv_id", "msg_id", "label"))
            for row in reader:
                message = Alert.load_message(row['conv_id'], row['msg_id'], message_dir)
                message.set_label(int(row['label']))
                messages.append(message)

        groundtruth.close()
        messages = messages[:500]
        return messages    

class AlertBasic(Alert):

    def __init__(self, test_percentage):
        self.train_test_split = TrainTestSplit()
        self.test_percentage = test_percentage /100

    def save_split(self):
        with open("train.csv", "w") as train_file:
            train_writer = csv.writer(train_file)
            for message in self.train_test_split.train:
                train_writer.writerow([message.id])
        train_file.close()
        with open("test.csv", "w") as test_file:
            test_writer = csv.writer(test_file)
            for message in self.train_test_split.test:
                test_writer.writerow([message.id])
        test_file.close()

    def fixed_split(self, corpus, train_file, test_file):
        train_ids = []
        with open(train_file, mode='r') as file:
            train_reader = csv.reader(file)
            for row in train_reader:
                train_ids.append(row[0])
        file.close()
        test_ids = []
        with open(test_file, mode='r') as file:
            test_reader = csv.reader(file)
            for row in test_reader:
                test_ids.append(row[0])
        file.close()

        train, test = [], []
        for message in corpus:
            if message.id in train_ids:
                train.append(message)
            elif message.id in test_ids:
                test.append(message)
        self.train_test_split.set_splits(train, test)

    def random_split(self, corpus):
        """Randomly divide the corpus into train and test splits. The test split's size is 
        based on --traintest-repartition parameter.

        Args:
         corpus: List of all messages.
        """
        random.shuffle(corpus)
        train_size = len(corpus) - round(len(corpus)*self.test_percentage)
        self.train_test_split.set_splits(corpus[:train_size], corpus[train_size:])

    def compute_features(self, feature_list):
        self.train_test_split.compute_features(feature_list)

    
    def train(self, model):
        self.train_test_split.train_model(model)

    def test(self):
        self.train_test_split.test_model()

    def evaluate(self, metric):
        metric.basic_evaluation(self.train_test_split)


class AlertCrossValidation(Alert):

    def __init__(self, cv_number, test_percentage):
        self.train_test_split = []
        self.test_percentage = test_percentage /100
        # number of folds in the cross validation
        self.cv_number = cv_number

    def random_split(self, corpus):
        random.shuffle(corpus)
        #Number of folds in the test subset
        test_folds_number = round(self.cv_number * (self.test_percentage))
        # Number of messages in a fold
        fold_size = round(len(corpus) / self.cv_number)
        if (0 < test_folds_number < self.cv_number):
            #cross validation with self.cv_number folds
            folds = []
            for i in range(self.cv_number):
                # all folds except last
                if i < self.cv_number-1:
                    fold = corpus[i*fold_size:(i+1)*fold_size-1]
                    folds.append(fold)
                # last fold
                else:
                    fold = corpus[i*fold_size:]
                    folds.append(fold)

            #generator returning the indexes of the test folds for each run of the cross validation
            gen = self.folds_generator(self.cv_number, test_folds_number)
            for test_folds in gen:
                train_test = TrainTestSplit()
                for i in range(len(folds)):
                    if i in test_folds:
                        train_test.test.extend(folds[i])
                    else:
                        train_test.train.extend(folds[i])
                self.train_test_split.append(copy.deepcopy(train_test))

    def folds_generator(self, nb_folds, nb_test_folds):
        folds = range(nb_folds)
        for i in range(nb_folds):
            ret = []
            for j in range(nb_test_folds):
                ret.append((folds[i]+j)%nb_folds)
            yield ret

    def fixed_split(self, corpus, train_file, test_file):
        for i in range(self.cv_number):
            self.train_test_split.append(TrainTestSplit())
        train_ids = {}
        with open(train_file, mode='r') as file:
            train_reader = csv.reader(file)
            for row in train_reader:
                if int(row[1]) not in train_ids:
                    train_ids[int(row[1])] = [row[0]]
                else:
                    train_ids[int(row[1])].append(row[0])
        file.close()
        test_ids = {}
        with open(test_file, mode='r') as file:
            test_reader = csv.reader(file)
            for row in test_reader:
                if int(row[1]) not in test_ids:
                    test_ids[int(row[1])] = [row[0]]
                else:
                    test_ids[int(row[1])].append(row[0])
        file.close()

        # for i in range(len(train_ids)):
        #     print (i, len(train_ids[i]))
        #     print (i, len(test_ids[i]))
        for message in corpus:
            for i in range(self.cv_number):
                if message.id in train_ids[i]:
                    self.train_test_split[i].train.append(copy.deepcopy(message))
                elif message.id in test_ids[i]:
                    self.train_test_split[i].test.append(copy.deepcopy(message))


    def save_split(self):
        with open("train.csv", "w") as train_file:
            train_writer = csv.writer(train_file)
            for i in range(len(self.train_test_split)):
                for message in self.train_test_split[i].train:
                    train_writer.writerow([message.id, i])
        train_file.close()
        with open("test.csv", "w") as test_file:
            test_writer = csv.writer(test_file)
            for i in range(len(self.train_test_split)):
                for message in self.train_test_split[i].test:
                    test_writer.writerow([message.id, i])
        test_file.close()

    def compute_features(self, feature_list):
        for split in self.train_test_split:
            split.compute_features(feature_list)

    def train(self, model):
        for split in self.train_test_split:
            new_model = copy.copy(model)
            split.train_model(new_model)

    def test(self):
        for split in self.train_test_split:
            split.test_model()

    def evaluate(self, metric):
        metric.cv_evaluation(self.train_test_split)