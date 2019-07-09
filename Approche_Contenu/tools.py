

import re, pickle, gzip
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

#Tokenize the message and return a list of tokens
def tokenize(message):
	words = message.split(" ")
	#Filter empty strings
	words = list(filter(None, words))
	return words

#Collapse the message when there are 3 or more identical consecutive characters
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

#Extract messages from file
# nb_mess = number of messages to load
def load_messages(fileName, nb_mess=-1):
	res = list()
	messages = zload(fileName)
	if nb_mess < 0:
		nb_mess = len(messages)
	

	for m in messages[:nb_mess]:
		#only text content of the message
		res.append(m[3])
	return res

#Extract and normalize messages from file
# nb_mess = number of messages to load
def load_messages_basic(fileName, nb_mess=-1):
	res = list()
	messages = zload(fileName)
	if nb_mess < 0:
		nb_mess = len(messages)
	for m in messages[:nb_mess]:
		#only text content of the message
		res.append(normalize_basic(m[3]))
	return res

#Dump object in a file
def zdump(obj, fileName):
    with gzip.open(fileName, "wb") as f:
        pickle.dump(obj, f, 2)

#Load a dumped object
def zload(fileName):
    with gzip.open(fileName, "rb") as f:
        items = pickle.load(f, encoding='latin-1')
        return items

#build a BoW from the corpus
def create_bow(corpus):
	vectorizer = CountVectorizer(encoding='latin-1')
	vectorizer = vectorizer.fit(corpus)
	return vectorizer

#Convert corpus to a matrix of tf-idf features
def create_tf_idf(corpus):
	vectorizer = TfidfVectorizer(encoding='latin-1')
	vectorizer = vectorizer.fit(corpus)
	return vectorizer

#Create a dictionnary mapping words to their frequencies in the corpus
def compute_word_frequency(corpus):
	dic = {}
	# [[]] -> []
	corpus = [y for x in corpus for y in x]
	for message in corpus:
		words = tokenize(message)
		for word in words:
			if word in dic:
			    dic[word] += 1
			else:
			    dic[word] = 1
	return dic

#Basic normalization
def normalize_basic(text):
	# Lowercase
	text = text.lower()
	# Tokenization using spaces
	tokens = tokenize(text)
	# Remove punctuation in all tokens
	for j,token in enumerate(tokens):
		tokens[j] = re.sub(r'[^\w\s]',' ',token)
	# Reassemble the message
	text = ' '.join(tokens)
	# Remove multiple spaces
	text = ' '.join(text.split())
	return text

#Split the corpus between abuse and non-abuse based on the labels
def split_abuse_nonabuse(corpus, labels):
	#2 distincts training corpus: corpus non abuse, corpus abuse
	corpus_non_abuse = []
	corpus_abuse = []
	#Get abuse and non-abuse messages thanks to the labels
	corpus_non_abuse = [corpus[i] for i in range(len(corpus)) if labels[i] == 0]
	corpus_abuse = [corpus[i] for i in range(len(corpus)) if labels[i] == 1]
	return corpus_non_abuse, corpus_abuse

#Generator for train, test set numbers for many-fold evaluation
def ranges_gen(size = 10, window = 3):
	n = 0
	while True:
		test = [v % size for v in range(n, n + window)]
		train = [v for v in range(size) if v not in test]
		yield (train, test)
		n += 1