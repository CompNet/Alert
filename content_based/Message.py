

class Message:

    def __init__(self, id, author, date, text):
        self.id = id
        self.author = author
        self.date = date
        self.text = text
        self.features = {}
        self.tmp_features = None

    def add_feature(self, fname, fvalue):
        self.features[fname] = fvalue

    def getText(self):
        return self.text

    def getFeatures(self):
        ret = list(self.features.values())
        return ret

    def set_tmp_features(self, tmp):
        self.tmp_features = tmp

class LabeledMessage(Message):

    def set_label(self, label):
        """Setter for the label.

        Args:
         label: Label of the message.
        """
        self.label = label

    def get_label(self):
        """Getter for the label.

        Returns:
         The label of the message.
        """
        return self.label