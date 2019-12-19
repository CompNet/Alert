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
        words = list(filter(None, words))
        return words

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
        text_corpus = [message[3] for message in message_corpus]
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

        for char in message[3]:
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
        total = len(message[3])
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

        message[2].update(features)

    @staticmethod
    def compute_word_frequency(corpus):
        dic = {}
        for message in corpus:
            words = Feature.tokenize(message[3])
            for word in words:
                if word in dic:
                    dic[word] += 1
                else:
                    dic[word] = 1
        return dic

    def create_abuse_nonabuse_dictionary(self, corpus):
        corpus_non_abuse = [message for message in corpus if int(message[4]) == 0]
        corpus_abuse = [message for message in corpus if int(message[4]) == 1]
        nonabuse_text = [message[3] for message in corpus_non_abuse]
        abuse_text = [message[3] for message in corpus_abuse]
        self.dic_non_abuse = Feature.compute_word_frequency(corpus_non_abuse)
        self.dic_abuse = Feature.compute_word_frequency(corpus_abuse)



class cLength(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            length = len(message[3])
            message[1].append(length)


class nWords(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            nb = len(words)
            message[1].append(nb)

class avgwLen(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            total_len = 0
            for word in words:
                total_len += len(word) 
            if len(words) > 0:
                avgLength = total_len*1.0 / len(words)
            else:
                avgLength = 0
            message[1].append(avgLength)

class uniqueChars(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            chars = set(message[3])
            nb_chars = len(chars)
            message[1].append(nb_chars)

class uniqueWords(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            nbwords = len(set(words))
            message[1].append(nbwords)

class collapseN(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            mess_len = len(message[3])
            collapsed_mess = Feature.collapse(message[3])
            collapsed_mess_len = len(collapsed_mess)
            nb = mess_len - collapsed_mess_len
            message[1].append(nb)

class longest(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            maxlen = -1
            for word in words:
                if (len(word) > maxlen):
                    maxlen = len(word)
            message[1].append(maxlen)

class cRatio(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            compressed = compress(message[3])
            base = len(message[3])
            if base > 0:
                ratio = len(compressed)*1.0 / base
            else:
                ratio = 1
            message[1].append(ratio)

class alpha(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['alpha'])

class alpha_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['alpha_r'])

class digit(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['digit'])

class digit_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['digit_r'])

class punctuation(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['punctuation'])

class punctuation_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['punctuation_r'])

class other(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['other'])

class other_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['other_r'])

class space(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['space'])

class space_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['space_r'])

class cap(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['cap'])

class cap_r(Feature):

    def compute(self, train_corpus, test_corpus):
        for message in train_corpus + test_corpus:
            if len(message[2]) == 0:
                Feature.compute_character_class(message)
            message[1].append(message[2]['cap_r'])


class nBadwords(Feature):

    def compute(self, train_corpus, test_corpus):
        with open("bad_words.txt", "r") as f:
            bad_words = []
            for line in f:
                bad_words.append(line.rstrip('\n'))
        f.close()
        for message in train_corpus + test_corpus:
            nb = 0
            words = Feature.tokenize(message[3])
            for word in words:
                if word in bad_words:
                    nb += 1
            message[1].append(nb)

class nHiddenBadwords(Feature):

    def compute(self, train_corpus, test_corpus):
        with open("bad_words.txt", "r") as f:
            bad_words = []
            for line in f:
                bad_words.append(line.rstrip('\n'))
        f.close()
        for message in train_corpus + test_corpus:
            nb = 0
            words = Feature.tokenize(Feature.collapse(message[3]))
            for word in words:
                if word in bad_words:
                    nb += 1
            message[1].append(nb)

class tfidf_nonabuse(Feature):

    def compute(self, train_corpus, test_corpus):
        corpus_non_abuse = [message for message in train_corpus if int(message[4]) == 0]
        tfidf_non_abuse = Feature.create_tf_idf(corpus_non_abuse)

        for message in train_corpus + test_corpus:
            score = tfidf_non_abuse.transform([message[3]])
            score_non_abuse = score.sum()
            message[1].append(score_non_abuse)

class tfidf_abuse(Feature):

    def compute(self, train_corpus, test_corpus):
        corpus_abuse = [message for message in train_corpus if int(message[4]) == 1]
        tfidf_abuse = Feature.create_tf_idf(corpus_abuse)

        for message in train_corpus + test_corpus:
            score = tfidf_abuse.transform([message[3]])
            score_abuse = score.sum()
            message[1].append(score_abuse)

class NB(Feature):

    def compute(self, train_corpus, test_corpus):
        bow = self.create_bow(train_corpus+test_corpus)
        train_text = [message[3] for message in train_corpus]
        train = bow.transform(train_text)
        train_labels = [int(message[4]) for message in train_corpus]
        clf = MultinomialNB()
        clf = clf.fit(train, train_labels)

        for message in train_corpus + test_corpus:
            test = bow.transform([message[3]])
            res = clf.predict_proba(test)
            message[1].append(res[0][1])

    #build a BoW from the corpus
    def create_bow(self, corpus):
        vectorizer = CountVectorizer()
        text_corpus = [message[3] for message in corpus]
        vectorizer = vectorizer.fit(text_corpus)
        return vectorizer

class posScore(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_non_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus+test_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            posScore = 0.0
            for word in words:
                if word in self.dic_non_abuse:
                    posScore += math.log(self.dic_non_abuse[word])
            message[1].append(posScore)

class negScore(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus+test_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            negScore = 0.0
            for word in words:
                if word in self.dic_abuse:
                    negScore += math.log(self.dic_abuse[word])
            message[1].append(negScore)

class posScore_collapsed(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_non_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus+test_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            posScore_collapsed = 0.0
            for word in words:
                word_collapsed = Feature.collapse(word)
                if word_collapsed in self.dic_non_abuse:
                    posScore_collapsed += math.log(self.dic_non_abuse[word_collapsed])
            message[1].append(posScore_collapsed)

class negScore_collapsed(Feature):

    def compute(self, train_corpus, test_corpus):
        if self.dic_abuse is None:
            self.create_abuse_nonabuse_dictionary(train_corpus+test_corpus)
        for message in train_corpus + test_corpus:
            words = Feature.tokenize(message[3])
            negScore_collapsed = 0.0
            for word in words:
                word_collapsed = Feature.collapse(word)
                if word_collapsed in self.dic_abuse:
                    negScore_collapsed += math.log(self.dic_abuse[word_collapsed])
            message[1].append(negScore_collapsed)