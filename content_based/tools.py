

import pickle, gzip, csv
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

#Dump object in a file
def zdump(obj, fileName):
    with gzip.open(fileName, "wb") as f:
        pickle.dump(obj, f, 2)

#Load a dumped object
def zload(fileName):
    with gzip.open(fileName, "rb") as f:
        items = pickle.load(f)
        return items

'''
Load message from file using conversation_id and message_id
Return: raw message and corresponding label
'''
def load_message(conv_id, message_id):
	with open("../Data/context/csv/%s.csv" % conv_id, mode='r') as csvfile:
		csv_reader = csv.DictReader(csvfile, fieldnames=("msg_id", "date", "author", "text"))
		for m in csv_reader:
			if m['msg_id'] == message_id:
				message = m['text']
		return message

#Tokenize the message and return a list of tokens
def tokenize(message):
	if isinstance(message, bytes):
		message = message.decode('latin1')
	message = str(message)
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

#Split the corpus between abuse and non-abuse based on the labels
def split_abuse_nonabuse(corpus, labels):
	#2 distincts training corpus: corpus non abuse, corpus abuse
	corpus_non_abuse = []
	corpus_abuse = []
	#Get abuse and non-abuse messages thanks to the labels
	corpus_non_abuse = [corpus[i] for i in range(len(corpus)) if labels[i] == 0]
	corpus_abuse = [corpus[i] for i in range(len(corpus)) if labels[i] == 1]
	return corpus_non_abuse, corpus_abuse

#Convert corpus to a matrix of tf-idf features
def create_tf_idf(corpus):
	vectorizer = TfidfVectorizer(encoding='latin-1')
	vectorizer = vectorizer.fit(corpus)
	return vectorizer

#build a BoW from the corpus
def create_bow(corpus):
	vectorizer = CountVectorizer(encoding='latin-1')
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

def folds_generator(nb_folds, nb_test_folds):
	folds = range(nb_folds)
	for i in range(nb_folds):
		ret = []
		for j in range(nb_test_folds):
			ret.append((folds[i]+j)%nb_folds)
		yield ret