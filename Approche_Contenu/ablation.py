# -*- coding: utf-8 -*- 
import copy, random, itertools
from tools import *
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from multiprocessing import Pool

import matplotlib
matplotlib.use('Agg')
#matplotlib.use("pdf")
import matplotlib.pyplot as plt

#Features importance estimator
def estimate_importance(features, labels):
	clf = ExtraTreesClassifier()
	clf = clf.fit(features, labels)
	return clf.feature_importances_


def compute_results(features_train, labels_train, features_test, labels_test):
	clf = SVC(class_weight='balanced')
	clf = CalibratedClassifierCV(clf)
	clf.fit(features_train,labels_train)
	res = clf.predict(features_test)

	ok = 0
	fp, fn = 0, 0
	tp, tn = 0, 0
	nAbuses = 0
	f1 = 0
	for r in range(len(res)):
		if res[r] == labels_test[r]:
			ok += 1
		if labels_test[r] == 1:
			if res[r] == 1:
				tp += 1
			if res[r] == 0:
				fn += 1
			nAbuses += 1
		if labels_test[r] == 0:
			if res[r] == 1:
				fp += 1
			if res[r] == 0:
				tn += 1

	rec = tp / float(nAbuses)
	pre = tp / float(tp + fp)
	if pre + rec > 0:
		f1 = 2 * (pre * rec) / float(pre + rec)
	return f1

if __name__ == '__main__':
	names = ['cLength', 'nWords', 'avgwLen', 'uniqueChars', 'uniqueWords', 'collapseN', 'longest', 'cRatio', 'nAlpha', 'rAlpha', 'nDigit', 'rDigit', 'nPunct', 'rPunct', 'nOther', 'rOther', 'nSpace', 'rSpace', 'nCap', 'rCap', 'nBadwords', 'nHiddenBadwords', 'tfidfPosScore', 'tfidfNegScore', 'posScore', 'negScore', 'cPosScore', 'cNegScore', 'NB']
	importance_feat = [0.0]*29
	imp_features = dict(zip(names, importance_feat))
	avg_pos_features = dict(zip(names, importance_feat))

	###### A VOIR #####
	fold = random.randint(0,9)
	features_train = zload("features/features_train_%s.pkl.gz" % fold)
	labels_train = zload("labels/labels_train_%s.pkl.gz" % fold)
	feature_names = list(names)
	###################

	#estimate importance of features
	estimates = estimate_importance(features_train, labels_train)
	feature_list = []
	for i, val in enumerate(estimates):
		feature_list.append((feature_names[i], val))
	#order from least to most important
	feature_list = sorted(feature_list, key=lambda x: x[1])

	#40 iteration
	nb_iteration = 40
	for it in range(nb_iteration):
		print it 
		f1s = [0]*29

		for k in range(10):
			feature_names = list(names)

			#load data/labels/scaler
			features_train = zload("features/features_train_%s.pkl.gz" % k)
			labels_train = zload("labels/labels_train_%s.pkl.gz" % k)
			features_test = zload("features/features_test_%s.pkl.gz" % k)
			labels_test = zload("labels/labels_test_%s.pkl.gz" % k)
			scaler = zload("models/scalers/scaler_%s.pkl.gz" % k)
			features_train = scaler.transform(features_train).tolist()
			features_test = scaler.transform(features_test).tolist()

			pool = Pool(processes=1)
			res = []
			nb_feat = len(feature_names)
			
			while nb_feat >= 1:
				res.append(pool.apply_async(compute_results, args=(copy.deepcopy(features_train), labels_train, copy.deepcopy(features_test), labels_test)))
				#Remove the least important feature
				#index of the feature to remove

				feat_to_remove = feature_list[len(names)-nb_feat][0]
				feat_index = feature_names.index(feat_to_remove)
				feature_names.remove(feat_to_remove)
				for f in features_train:
					del f[feat_index]
				for f in features_test:
					del f[feat_index]
				nb_feat -= 1

			i = 0
			for r in res:
				f1 = r.get()
				#Resultat pour 1 iteration
				f1s[i] += f1
				i += 1
			

			pool.close()
			pool.join()
			
		#Sauvegarde l'ordre dans lequel les features ont été suppr pendant ce run
		f = open("ablation/text/run_%s.txt" % it, "w")
		res_list = [x[0] for x in feature_list]
		f.write(str(res_list))

		f1s = [x / 10 for x in f1s]
		####### TRANSFORMATION POUR FAIRE COMME EP 
		#liste des features dans l'ordre dans lequel elles sont suppr
		f_names = [v[0] for v in feature_list]
		#écart de f-mesure lorsque chaque feature est enlevée
		f1s_loss = [f1s[i] - f1s[i+1] for i in range(len(f1s)-1)]
		feature_importance_update = zip(f_names, f1s_loss)
		#Rajoute la dernière feature (la plus importante qui n'a pas été supprimée)
		feature_importance_update.append((f_names[-1], 65.0))
		#order
		for i in range(it%2, len(feature_importance_update)-1, 2):
			if feature_importance_update[i][1] > feature_importance_update[i+1][1]:
				tmp = feature_importance_update[i]
				feature_importance_update[i] = feature_importance_update[i+1]
				feature_importance_update[i+1] = tmp

		#feature_importance_update = sorted(feature_importance_update, key=lambda x: x[1])
		feature_list = feature_importance_update

		#Sauvegarde la f-mesure moyenne perdue à chaque fois qu'on retire chaque feature
		cpt = 29
		for val in feature_importance_update:
			imp_features[val[0]] += val[1]
			# Saubegarde la position moyenne de la feature
			avg_pos_features[val[0]] += cpt
			cpt -= 1
		##############
		# marker='o'
		plt.plot(f1s, color='red', linewidth=1)
		plt.ylabel('F1-Score')
		plt.xlabel('Number Of Features Removed')
		#plt.xticks(range(0,29,2))
		plt.savefig("ablation/run_%s.png" % it)
		plt.close()


	'''plt.plot(f1s, color='red', linewidth=1)	
	plt.ylabel('F1-Score')
	plt.xlabel('Number Of Features Removed')
	plt.savefig("features/F1score.pdf")'''
		
	print 'PERTE DE F-MESURE MOYENNE DUE AU RETRAIT DE CETTE FEATURE'
	for key, value in sorted(imp_features.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		print "%s: %s" % (key, value/nb_iteration)
	print '-------------'
	print 'POSITION MOYENNE DE LA FEATURE'
	for key, value in sorted(avg_pos_features.iteritems(), key=lambda (k,v): (v,k)):
		print "%s: %s" % (key, value/nb_iteration)