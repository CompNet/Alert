#!/usr/bin/python -u
# -*- coding: utf-8 -*- 

from tools import *
from features import *
from metrics import *
import csv, random

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import argparse as ap


'''
Computes and returns features for test and train messages
'''
def compute_all_features(messages_train, messages_test, Y_train, Y_test):
	features_train = []
	for i in range(len(messages_train)):
		features_part = []
		for message in messages_train[i]:
			features_msg = compute_morphological_features(message)
			features_part.append(features_msg)
		features_train.append(features_part)
	
		tfidfPosScore, tfidfNegScore = tfidf_scores(messages_train[i], Y_train[i], messages_train[i])
		posScore, negScore, cPosScore, cNegScore = comment_polarization_scores(messages_train[i], Y_train[i], messages_train[i])
		NB = compute_naive_bayes(messages_train[i], Y_train[i], messages_train[i])
		for j in range(len(features_train[i])):
			features_train[i][j].extend([tfidfPosScore[j], tfidfNegScore[j], posScore[j], negScore[j], cPosScore[j], cNegScore[j], NB[j]])
	
	features_test = []
	for i in range(len(messages_test)):
		features_part = []
		for message in messages_test[i]:
			features_msg = compute_morphological_features(message)
			features_part.append(features_msg)
		features_test.append(features_part) 

		tfidfPosScore, tfidfNegScore = tfidf_scores(messages_train[i], Y_train[i], messages_test[i])
		posScore, negScore, cPosScore, cNegScore = comment_polarization_scores(messages_train[i], Y_train[i], messages_test[i])
		NB = compute_naive_bayes(messages_train[i], Y_train[i], messages_test[i])
		for j in range(len(features_test[i])):
			features_test[i][j].extend([tfidfPosScore[j], tfidfNegScore[j], posScore[j], negScore[j], cPosScore[j], cNegScore[j], NB[j]])

	return features_train, features_test

	

# Load messages and labels from files
def load_data():
	messages = []
	labels = []
	with open("../Data/context/groundtruth.csv", mode='r') as groundtruth_file:
		csv_reader = csv.DictReader(groundtruth_file, fieldnames=("conv_id", "msg_id", "label"))
		for row in csv_reader:
			message = load_message(row['conv_id'], row['msg_id'])
			messages.append(message)
			labels.append(int(row['label']))
	
	groundtruth_file.close()
	# shuffle lists
	l = list(zip(messages, labels))
	random.shuffle(l)
	messages, labels = zip(*l)
	return messages, labels

#Creates and returns classifier
def create_classifier():
	svc = SVC(class_weight='balanced', probability=True)
	return svc

# Generates models and scalers 
def generate_model(X_train, Y_train):
	models, scalers = [], []
	for i in range(len(X_train)):
		# Scaler/Model
		scaler = StandardScaler().fit(X_train[i])
		X_train_scaled = scaler.transform(X_train[i]).tolist()

		clf = create_classifier()
		clf.fit(X_train_scaled,Y_train[i])
		models.append(clf)
		scalers.append(scaler)
	return models, scalers

# Compute results
def compute_results(models,scalers, X_test, Y_true):

	predictions = []
	# len(models) = len(scalers) = len(X_test) = len(Y_test)
	for i in range(len(models)):
		features = scalers[i].transform(X_test[i])
		Y_pred = models[i].predict(features)
		predictions.append(Y_pred)

	print (compute_f_measure(Y_true, predictions))
	


if __name__ == '__main__':
	p = ap.ArgumentParser()
	p.add_argument("-m", "--validation-method", choices=["basic", "cv"], help="Validation method to use: basic or cross validation", type = str, default = 'basic')
	p.add_argument("-s", "--cv-size", help="Number of folds to use in the cross validation", type = int, default = 10)
	p.add_argument("-r", "--cv-repartition", help="Pencentage of folds to use in the test subset", type = int, default = 30)
	args = p.parse_args()

	messages, labels = load_data()
	messages_train, messages_test, Y_train, Y_test = [], [], [], []
	if args.validation_method == 'basic':
		xtrain, xtest, ytrain, ytest = train_test_split(messages, labels, test_size=0.3)
		messages_train.append(xtrain)
		messages_test.append(xtest)
		Y_train.append(ytrain)
		Y_test.append(ytest)
	elif args.validation_method == 'cv':
		#cross validation with args.cv_size folds
		test_folds_number = round(args.cv_size * (args.cv_repartition / 100))
		fold_size = round(len(messages) / args.cv_size)
		if (0 < test_folds_number < args.cv_size):
			message_folds, label_folds = [], []
			# split corpus into args.cv_size folds
			for i in range(args.cv_size):
				# all folds except last
				if i < args.cv_size-1:
					fold = messages[i*fold_size:(i+1)*fold_size-1]
					fold_labels = labels[i*fold_size:(i+1)*fold_size-1]
					message_folds.append(fold)
					label_folds.append(fold_labels)
				# last fold
				else:
					fold = messages[i*fold_size:]
					fold_labels = labels[i*fold_size:]
					message_folds.append(fold)
					label_folds.append(fold_labels)

			#generator returning the indexes of the test folds for each run of the cross validation
			gen = folds_generator(args.cv_size, test_folds_number)

			for test_folds in gen:
				msg_test_tmp, lab_test_tmp = [], []
				msg_train_tmp, lab_train_tmp = [], []
				for i in range(len(message_folds)):
					if i in test_folds:
						msg_test_tmp.extend(message_folds[i])
						lab_test_tmp.extend(label_folds[i])
					else:
						msg_train_tmp.extend(message_folds[i])
						lab_train_tmp.extend(label_folds[i])
				messages_test.append(msg_test_tmp)
				Y_test.append(lab_test_tmp)
				messages_train.append(msg_train_tmp)
				Y_train.append(lab_train_tmp)

	X_train, X_test = compute_all_features(messages_train, messages_test, Y_train, Y_test)
	models, scalers = generate_model(X_train, Y_train)
	compute_results(models,scalers, X_test, Y_test)

