import string
import math
from abc import ABC, abstractmethod
from .lzw import compress
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class Feature(ABC):

    def __init__(self):
        self.dic_abuse = None
        self.dic_non_abuse = None

    @abstractmethod
    def compute(self, train_corpus, test_corpus):
        pass

    @staticmethod
    def tokenize(message):
        words = message.split(" ")
        #Filter empty strings
        res = [x for x in words if x != None]
        return res

    #Collapse the message when there are 3 or more identical consecutive characters
    @staticmethod
    def collapse(message):
        out = ""
        prev = None
        prevprev = None
        for c in message:
            if not c == prev == prevprev:
                out += c
            prevprev = prev
            prev = c
        return out

    #Convert corpus to a matrix of tf-idf features
    @staticmethod
    def create_tf_idf(message_corpus):
        vectorizer = TfidfVectorizer()
        text_corpus = [message.getText() for message in message_corpus]
        vectorizer = vectorizer.fit(text_corpus)
        return vectorizer

    @staticmethod
    def compute_character_class(message):
        features = {}
        alpha = 0
        digit = 0
        punctuation = 0
        other = 0
        space = 0
        cap = 0

        for char in message.getText():
            if char.isupper():
                cap += 1
            if char.isalpha():
                alpha += 1
            elif char.isdigit():
                digit += 1
            elif char.isspace():
                space += 1
            elif char in string.punctuation:
                punctuation += 1
            else:
                other += 1
        #ratios
        total = len(message.getText())
        if total > 0:
            features['alpha_r'] = alpha*1.0 / total
            features['digit_r'] = digit*1.0 / total
            features['punctuation_r'] = punctuation*1.0 / total
            features['other_r'] = other*1.0 / total
            features['space_r'] = space*1.0 / total
            features['cap_r'] = cap*1.0 / total
        else:
            features['alpha_r'] = 0
            features['digit_r'] = 0
            features['punctuation_r'] = 0
            features['other_r'] = 0
            features['space_r'] = 0
            features['cap_r'] = 0

        features['alpha'] = alpha
        features['digit'] = digit
        features['punctuation'] = punctuation
        features['other'] = other
        features['space'] = space
        features['cap'] = cap
        message.set_tmp_features(features)

    @staticmethod
    def compute_word_frequency(corpus):
        dic = {}
        for message in corpus:
            words = Feature.tokenize(message.getText())
            for word in words:
                if word in dic:
                    dic[word] += 1
                else:
                    dic[word] = 1
        return dic

    def create_abuse_nonabuse_dictionary(self, corpus):
        corpus_non_abuse = [message for message in corpus if message.label == 0]
        corpus_abuse = [message for message in corpus if message.label == 1]
        nonabuse_text = [message.getText() for message in corpus_non_abuse]
        abuse_text = [message.getText() for message in corpus_abuse]
        self.dic_non_abuse = Feature.compute_word_frequency(corpus_non_abuse)
        self.dic_abuse = Feature.compute_word_frequency(corpus_abuse)



class cLength(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            length = len(message.getText())
            message.add_feature("cLength", length)


class nWords(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            nb = len(words)
            message.add_feature("nWords", nb)

class avgwLen(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            total_len = 0
            for word in words:
                total_len += len(word) 
            if len(words) > 0:
                avgLength = total_len*1.0 / len(words)
            else:
                avgLength = 0
            message.add_feature("avgwLen", avgLength)

class uniqueChars(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            chars = set(message.getText())
            nb_chars = len(chars)
            message.add_feature("uniqueChars", nb_chars)

class uniqueWords(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            nbwords = len(set(words))
            message.add_feature("uniqueWords", nbwords)

class collapseN(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            mess_len = len(message.getText())
            collapsed_mess = Feature.collapse(message.getText())
            collapsed_mess_len = len(collapsed_mess)
            nb = mess_len - collapsed_mess_len
            message.add_feature("collapseN", nb)

class longest(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            maxlen = -1
            for word in words:
                if (len(word) > maxlen):
                    maxlen = len(word)
            message.add_feature("longest", maxlen)

class cRatio(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            compressed = compress(message.getText())
            base = len(message.getText())
            if base > 0:
                ratio = len(compressed)*1.0 / base
            else:
                ratio = 1
            message.add_feature("cRatio", ratio)

class alpha(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("alpha", message.tmp_features['alpha'])

class alpha_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("alpha_r", message.tmp_features['alpha_r'])

class digit(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("digit", message.tmp_features['digit'])

class digit_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("digit_r", message.tmp_features['digit_r'])

class punctuation(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("punctuation", message.tmp_features['punctuation'])

class punctuation_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("punctuation_r", message.tmp_features['punctuation_r'])

class other(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("other", message.tmp_features['other'])

class other_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("other_r", message.tmp_features['other_r'])

class space(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("space", message.tmp_features['space'])

class space_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("space_r", message.tmp_features['space_r'])

class cap(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("cap", message.tmp_features['cap'])

class cap_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if message.tmp_features is None:
                Feature.compute_character_class(message)
            message.add_feature("cap_r", message.tmp_features['cap_r'])


class nBadwords(Feature):

    def compute(self, train_corpus, test_corpus):
        with open("bad_words.txt", "r") as f:
            bad_words = []
            for line in f:
                bad_words.append(line.rstrip('\n'))
        f.close()
        for message in train_corpus + test_corpus:
            nb = 0
            words = Feature.tokenize(message.getText())
            for word in words:
                if word in bad_words:
                    nb += 1
            message.add_feature("nBadwords", nb)

class nHiddenBadwords(Feature):

    def compute(self, train_corpus, test_corpus):
        with open("bad_words.txt", "r") as f:
            bad_words = []
            for line in f:
                bad_words.append(line.rstrip('\n'))
        f.close()
        for message in train_corpus + test_corpus:
            nb = 0
            words = Feature.tokenize(Feature.collapse(message.getText()))
            for word in words:
                if word in bad_words:
                    nb += 1
            message.add_feature("nHiddenBadwords", nb)

class tfidf_nonabuse(Feature):

    def compute(self, train_corpus, test_corpus):
        corpus_non_abuse = [message for message in train_corpus if message.label == 0]
        tfidf_non_abuse = Feature.create_tf_idf(corpus_non_abuse)

        for message in train_corpus + test_corpus:
            score = tfidf_non_abuse.transform([message.getText()])
            score_non_abuse = score.sum()
            message.add_feature("tfidf_nonabuse", score_non_abuse)

class tfidf_abuse(Feature):

    def compute(self, train_corpus, test_corpus):
        corpus_abuse = [message for message in train_corpus if message.label == 1]
        tfidf_abuse = Feature.create_tf_idf(corpus_abuse)

        for message in train_corpus + test_corpus:
            score = tfidf_abuse.transform([message.getText()])
            score_abuse = score.sum()
            message.add_feature("tfidf_abuse", score_abuse)

class NB(Feature):

    def compute(self, train_corpus, test_corpus):
        bow = self.create_bow(train_corpus+test_corpus)
        train_text = [message.getText() for message in train_corpus]
        train = bow.transform(train_text)
        train_labels = [message.get_label() for message in train_corpus]
        clf = MultinomialNB()
        clf = clf.fit(train, train_labels)

        for message in train_corpus + test_corpus:
            test = bow.transform([message.getText()])
            res = clf.predict_proba(test)
            message.add_feature("NB", res[0][1])

    #build a BoW from the corpus
    def create_bow(self, corpus):
        vectorizer = CountVectorizer()
        text_corpus = [message.getText() for message in corpus]
        vectorizer = vectorizer.fit(text_corpus)
        return vectorizer

class posScore(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_non_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            posScore = 0.0
            for word in words:
                if word in self.dic_non_abuse:
                    posScore += math.log(self.dic_non_abuse[word])
            message.add_feature("posScore", posScore)

class negScore(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            negScore = 0.0
            for word in words:
                if word in self.dic_abuse:
                    negScore += math.log(self.dic_abuse[word])
            message.add_feature("negScore", negScore)

class posScore_collapsed(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_non_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            posScore_collapsed = 0.0
            for word in words:
                word_collapsed = Feature.collapse(word)
                if word_collapsed in self.dic_non_abuse:
                    posScore_collapsed += math.log(self.dic_non_abuse[word_collapsed])
            message.add_feature("posScore_collapsed", posScore_collapsed)

class negScore_collapsed(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message.getText())
            negScore_collapsed = 0.0
            for word in words:
                word_collapsed = Feature.collapse(word)
                if word_collapsed in self.dic_abuse:
                    negScore_collapsed += math.log(self.dic_abuse[word_collapsed])
            message.add_feature("negScore_collapsed", negScore_collapsed)