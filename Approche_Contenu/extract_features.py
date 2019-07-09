#!/usr/bin/python -u
# -*- coding: utf-8 -*- 

from tools import *
from lzw import *
import string, math
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB


#Number of characters in the message
def message_length_char(message):
	res = len(message)
	return res

#Number of words in the message
def message_length_word(message):
	words = tokenize(message)
	return len (words)

#Average length of words in the message 
def average_word_length(message):
	words = tokenize(message)
	total_len = 0
	for word in words:
		total_len = total_len + len(word) 
	if len(words) > 0:
		return total_len*1.0 / len(words)
	return 0

#Number of distincts characters in the message
def unique_characters_number(message):
	chars = set(message)
	return len(chars)

#Number of distincts words in the message
def unique_words_number(message):
	words = tokenize(message)
	words = set(words)
	return len(words)

#Number of collapsed characters in the message
def collapsed_characters_number(message):
	mess_len = message_length_char(message)
	collapsed_mess = collapse(message)
	collapsed_mess_len = len(collapsed_mess)
	return mess_len-collapsed_mess_len 

#Length of the longest word in the message
def longest_word(message):
	words = tokenize(message)
	maxlen = -1
	for word in words:
		if (len(word) > maxlen):
			maxlen = len(word)
	return maxlen

#Ratio of the length of the compressed message to that of the original message. Relates to the number of copy pastes in the message
def compression_ratio(message):
	compressed = compress(message)
	base = message_length_char(message)
	if base > 0:
		return len(compressed)*1.0 / base
	return 1

#Number of characters and ratio for each of the 6 classes : Alpha, Digit, Punctuation, Other, Space, Cap
def character_classes(message):
	alpha = 0
	digit = 0
	punctuation = 0
	other = 0
	space = 0
	cap = 0

	for c in message:
		if c.isupper():
			cap += 1
		if c.isalpha():
			alpha += 1
		elif c.isdigit():
			digit += 1
		elif c.isspace():
			space += 1
		elif c in string.punctuation:
			punctuation += 1
		else:
			other += 1
	#ratios
	total = message_length_char(message)
	if total > 0:
		alpha_r = alpha*1.0 / total
		digit_r = digit*1.0 / total
		punctuation_r = punctuation*1.0 / total
		other_r = other*1.0 / total
		space_r = space*1.0 / total
		cap_r = cap*1.0 / total
		return alpha, alpha_r, digit, digit_r, punctuation, punctuation_r, other, other_r, space, space_r, cap, cap_r
	#Messages without text
	return 0,0,0,0,0,0,0,0,0,0,0,0

#Number of bad words in the message
def bad_words_number(message):
	with open("bad_words.txt", "r") as f:
		bad_words = []
		for line in f:
			bad_words.append(line.rstrip('\n'))
	f.close()

	nb = 0
	words = tokenize(message)
	for word in words:
		if word in bad_words:
			nb += 1
	return nb

#Naive Bayes
def compute_naive_bayes(folds_train, labels_train, folds_test):
	NB_score = [[] for x in range(10)]
	for k in range(10):

		bow = create_bow(folds_train[k]+folds_test[k])
		train = bow.transform(folds_train[k])
		test = bow.transform(folds_test[k])

		clf = MultinomialNB()
		clf = clf.fit(train, labels_train[k])
		res = clf.predict_proba(test)
		#Proba of being abusive
		res = [[column[1]] for column in res]

		NB_score[k] = res
	return NB_score

	
#Scores based on the frequency of words in the messages accross abuse and non-abuse corpus
def comment_polarization_scores(folds_train, labels_train, folds_test):
	pos_score = [[] for x in range(10)]
	neg_score = [[] for x in range(10)]
	pos_score_collapsed = [[] for x in range(10)]
	neg_score_collapsed = [[] for x in range(10)]
	for k in range(10):
		corpus_non_abuse, corpus_abuse = split_abuse_nonabuse(folds_train[k], labels_train[k])
		dic_non_abuse = compute_word_frequency(corpus_non_abuse)
		dic_abuse = compute_word_frequency(corpus_abuse)

		for message in folds_test[k]:
			words = tokenize(message)
			posScore = 0.0
			negScore = 0.0
			posScore_c = 0.0
			negScore_c = 0.0
			for word in words:
				if word in dic_non_abuse:
					posScore += math.log(dic_non_abuse[word])
				if word in dic_abuse:
					negScore += math.log(dic_abuse[word])
				word_collapsed = collapse(word)
				if word_collapsed in dic_non_abuse:
					posScore_c += math.log(dic_non_abuse[word_collapsed])
				if word_collapsed in dic_abuse:
					negScore_c += math.log(dic_abuse[word_collapsed])
			pos_score[k].append([posScore])
			neg_score[k].append([negScore])
			pos_score_collapsed[k].append([posScore_c])
			neg_score_collapsed[k].append([negScore_c])

	return pos_score, neg_score, pos_score_collapsed, neg_score_collapsed

#Scores based on tf-idf of words in message relatively to abuse and non-abuse class
def tfidf_scores(folds_train, labels_train, folds_test):
	#res_non_abuse = score for non-abuse class, res_abuse = score for abuse class
	res_non_abuse = [[] for x in range(10)]
	res_abuse = [[] for x in range(10)]
	for k in range(10):
		#2 distincts training corpus: corpus non abuse, corpus abuse
		corpus_non_abuse, corpus_abuse = split_abuse_nonabuse(folds_train[k], labels_train[k])
		
		tfidf_non_abuse = create_tf_idf(corpus_non_abuse)
		tfidf_abuse = create_tf_idf(corpus_abuse)

		#Each message in the test fold
		for m in folds_test[k]:
			score0 = tfidf_non_abuse.transform([m])
			res_non_abuse[k].append([score0.sum()])
			score1 = tfidf_abuse.transform([m])
			res_abuse[k].append([score1.sum()])

	return res_non_abuse, res_abuse

#Computes morphological features for the message 
def compute_features(message):
	features_msg = []
	cLength = message_length_char(message)
	nWords = message_length_word(message)
	avgwLen = average_word_length(message)
	uniqueChars = unique_characters_number(message)
	uniqueWords = unique_words_number(message)
	collapseN = collapsed_characters_number(message)
	longest = longest_word(message)
	cRatio = compression_ratio(message)
	nAlpha, rAlpha, nDigit, rDigit, nPunct, rPunct, nOther, rOther, nSpace, rSpace, nCap, rCap = character_classes(message)
	nBadwords = bad_words_number(message)
	nHiddenBadwords = bad_words_number(collapse(message))
	
	features_msg.extend((cLength, nWords, avgwLen, uniqueChars, uniqueWords, collapseN, longest, cRatio, nAlpha, rAlpha, nDigit, rDigit, nPunct, rPunct, nOther, rOther, nSpace, rSpace, nCap, rCap, nBadwords, nHiddenBadwords))
	#features_msg.extend((rCap,))
	return features_msg

#Compute and save features for each fold
def compute_all_features(folds_train, labels_train, folds_test, labels_test):
	features_train = [list()]*10
	features_test = [list()]*10
	
	for k in range(10):
		all_features_train = []
		all_features_test = []

		for message in folds_train[k]:
			features_msg = compute_features(message)
			all_features_train.append(features_msg)
		features_train[k] = all_features_train

		for message in folds_test[k]:
			features_msg = compute_features(message)
			all_features_test.append(features_msg)
		features_test[k] = all_features_test

	tfidfPosScore, tfidfNegScore = tfidf_scores(folds_train, labels_train, folds_test)
	posScore, negScore, cPosScore, cNegScore = comment_polarization_scores(folds_train, labels_train, folds_test)
	NB = compute_naive_bayes(folds_train, labels_train, folds_test)
	for k in range(10):
		for i in range(len(features_test[k])):
			features_test[k][i] += tfidfPosScore[k][i] + tfidfNegScore[k][i] + posScore[k][i] + negScore[k][i] + cPosScore[k][i] + cNegScore[k][i] + NB[k][i]
			#features_test[k][i] += tfidfPosScore[k][i] + NB[k][i]

	tfidfPosScore, tfidfNegScore = tfidf_scores(folds_train, labels_train, folds_train)
	posScore, negScore, cPosScore, cNegScore = comment_polarization_scores(folds_train, labels_train, folds_train)
	NB = compute_naive_bayes(folds_train, labels_train, folds_train)
	for k in range(10):
		for i in range(len(features_train[k])):
			features_train[k][i] += tfidfPosScore[k][i] + tfidfNegScore[k][i] + posScore[k][i] + negScore[k][i] + cPosScore[k][i] + cNegScore[k][i] + NB[k][i]
			#features_train[k][i] += tfidfPosScore[k][i] + NB[k][i]

	#save features and labels
	for k in range(10):
		zdump(features_test[k], "features/features_test_%s.pkl.gz" % (k))
		zdump(features_train[k], "features/features_train_%s.pkl.gz" % (k))
		zdump(labels_test[k], "labels/labels_test_%s.pkl.gz" % (k))
		zdump(labels_train[k], "labels/labels_train_%s.pkl.gz" % (k))
	print ("%s features used" % len(features_test[0][0]))

#Creates folds for cross validation
def create_folds():
	folds_train = [list()]*10
	folds_test = [list()]*10
	labels_test = [list()]*10
	labels_train = [list()]*10
	g = ranges_gen()
	for k in range(10):
		train, test = next(g)
		for p in train:
			messages_abuse = load_messages("../Data/10-Split/abuses_messages.1.s.pkl.gz-%s" % p)
			messages_non_ab = load_messages("../Data/10-Split/abuses_messages.0.s.pkl.gz-%s" % p, nb_mess=len(messages_abuse)+1)
			messages = messages_abuse + messages_non_ab
			folds_train[k] = folds_train[k] + messages
			labels_train[k] = labels_train[k] + [0]*len(messages_non_ab) + [1]*len(messages_abuse)

		for p in test:
			messages_abuse = load_messages("../Data/10-Split/abuses_messages.1.s.pkl.gz-%s" % p)
			messages_non_ab = load_messages("../Data/10-Split/abuses_messages.0.s.pkl.gz-%s" % p, nb_mess=len(messages_abuse)+1)
			messages = messages_abuse + messages_non_ab
			folds_test[k] = folds_test[k] + messages
			labels_test[k] = labels_test[k] + [0]*len(messages_non_ab) + [1]*len(messages_abuse)

	return folds_train, labels_train, folds_test, labels_test


if __name__ == '__main__':
	folds_train, labels_train, folds_test, labels_test = create_folds()
	compute_all_features(folds_train, labels_train, folds_test, labels_test)
