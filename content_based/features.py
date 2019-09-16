from tools import *
from lzw import *
import string, math
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

	if isinstance(message, bytes):
		message = message.decode('latin1')
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

#Scores based on tf-idf of words in message relatively to abuse and non-abuse class
def tfidf_scores(X_train, y_train, messages):
	score_abuse = []
	#2 distincts training corpus: corpus non abuse, corpus abuse
	corpus_non_abuse, corpus_abuse = split_abuse_nonabuse(X_train, y_train)
		
	tfidf_non_abuse = create_tf_idf(corpus_non_abuse)
	tfidf_abuse = create_tf_idf(corpus_abuse)

	non_abuse = []
	abuse = []
	for message in messages:
		#score_non_abuse = score for non-abuse class, score_abuse = score for abuse class
		score0 = tfidf_non_abuse.transform([message])
		score_non_abuse = score0.sum()
		score1 = tfidf_abuse.transform([message])
		score_abuse = score1.sum()
		non_abuse.append(score_non_abuse)
		abuse.append(score_abuse)

	return non_abuse, abuse

#Scores based on the frequency of words in the messages accross abuse and non-abuse corpus
def comment_polarization_scores(X_train, y_train, messages):
	corpus_non_abuse, corpus_abuse = split_abuse_nonabuse(X_train, y_train)
	dic_non_abuse = compute_word_frequency(corpus_non_abuse)
	dic_abuse = compute_word_frequency(corpus_abuse)

	r_posScore = []
	r_negScore = []
	r_posScore_collapsed = []
	r_negScore_collapsed = []
	for message in messages:
		words = tokenize(message)
		posScore = 0.0
		negScore = 0.0
		posScore_collapsed = 0.0
		negScore_collapsed = 0.0
		for word in words:
			if word in dic_non_abuse:
				posScore += math.log(dic_non_abuse[word])
			if word in dic_abuse:
				negScore += math.log(dic_abuse[word])
			word_collapsed = collapse(word)
			if word_collapsed in dic_non_abuse:
				posScore_collapsed += math.log(dic_non_abuse[word_collapsed])
			if word_collapsed in dic_abuse:
				negScore_collapsed += math.log(dic_abuse[word_collapsed])
		r_posScore.append(posScore)
		r_negScore.append(negScore)
		r_posScore_collapsed.append(posScore_collapsed)
		r_negScore_collapsed.append(negScore_collapsed)

	return r_posScore, r_negScore, r_posScore_collapsed, r_negScore_collapsed


#Naive Bayes
def compute_naive_bayes(X_train, y_train, messages):
	bow = create_bow(X_train+messages)
	train = bow.transform(X_train)
	test = bow.transform(messages)

	clf = MultinomialNB()
	clf = clf.fit(train, y_train)
	res = clf.predict_proba(test)

	#Proba of being abusive
	NB_score = []
	for column in res:
		NB_score.append(column[1])
	return NB_score

#Computes morphological features for the message 
def compute_morphological_features(message):
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

	return features_msg
