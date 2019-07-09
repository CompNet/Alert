#!/usr/bin/python -u

from tools import *
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt 

# Create and save models
def generate_models():
	for k in range(10):
		# Load data
		features_train = zload("features/features_train_%s.pkl.gz" % k)
		labels_train = zload("labels/labels_train_%s.pkl.gz" % k)

		# Model
		scaler = StandardScaler().fit(features_train)
		features_scaled = scaler.transform(features_train).tolist()

		clf = SVC(class_weight='balanced', probability=True)
		clf.fit(features_scaled,labels_train)
		
		# Save scaler and model
		zdump(scaler, "models/scalers/scaler_%s.pkl.gz" % (k))
		zdump(clf, "models/model_%s.pkl.gz" % (k))

# Compute results for 10-fold cross validation 
def compute_10fold_results(threshold):
	scores = {k : [] for k in ['rec', 'fp', 'fn', 'tp', 'tn', 'acc', 'f1']}
	for k in range(10):
		# Load data
		features_test = zload("features/features_test_%s.pkl.gz" % k)
		labels_test = zload("labels/labels_test_%s.pkl.gz" % k)
		# Load classifier
		clf = zload("models/model_%s.pkl.gz" % (k))
		rec, pre, fp, fn, tp, tn, acc, f1 = compute_results(k, clf, features_test, labels_test, threshold)

		scores['rec'].append(rec)
		leny = fp + fn + tp + tn
		scores['fp'].append(fp / float(leny))
		scores['fn'].append(fn / float(leny))
		scores['tp'].append(tp / float(leny))
		scores['tn'].append(tn / float(leny))
		scores['acc'].append(acc)
		scores['f1'].append(f1)

	rec = sum(scores['rec']) / len(scores['rec'])
	afp = sum(scores['fp']) / len(scores['fp'])
	afn = sum(scores['fn']) / len(scores['fn'])
	atp = sum(scores['tp']) / len(scores['tp'])
	atn = sum(scores['tn']) / len(scores['tn'])
	aacc = sum(scores['acc']) / len(scores['acc'])
	pre = atp / (atp + afp)
	af1 = sum(scores['f1']) / len(scores['f1'])
	return rec, pre, afp, afn, atp, atn, aacc, af1

# Compute results
def compute_results(k, classifier, features, Y_true, threshold):
	scaler = zload("models/scalers/scaler_%s.pkl.gz" % (k))
	features = scaler.transform(features)
	#Y_pred = classifier.predict(features)

	# save probabilities
	out_probas = classifier.predict_proba(features)
	f = open("output/probas_%s.txt" % k, "w")
	# probability of each message to be in abuse class
	probas = [column[1] for column in out_probas]
	f.write(str(probas))
	f.close()

	############
	# Use custom threshold
	Y_pred = [] 
	for val in probas:
		if val > threshold:
			Y_pred.append(1)
		else:
			Y_pred.append(0)
	############

	ok = 0
	fp, fn = 0, 0
	tp, tn = 0, 0
	nAbuses = 0
	for r in range(len(Y_pred)):
		if Y_pred[r] == Y_true[r]:
			ok += 1
		if Y_true[r] == 1:
			if Y_pred[r] == 1:
				tp += 1
			if Y_pred[r] == 0:
				fn += 1
			nAbuses += 1
		if Y_true[r] == 0:
			if Y_pred[r] == 1:
				fp += 1
			if Y_pred[r] == 0:
				tn += 1

	rec = tp / float(nAbuses)
	pre = tp / float(tp + fp)
	acc = ok / float(len(Y_pred))
	f1 = f1_score(Y_true, Y_pred, average='binary', pos_label=1)
	return rec, pre, fp, fn, tp, tn, acc, f1


if __name__ == '__main__':
	generate_models()
	x = [] 
	y_f1 = []
	y_pre = []
	y_rec = []
	threshold = 0.01
	while threshold <=1:
		print (threshold)
		rec, pre, afp, afn, atp, atn, acc, f1 = compute_10fold_results(threshold)
		print ("Average F-measure: %s" % f1)
		print ("Average Precision: %0.4f" % pre)
		print ("Average Recall: %0.4f" % rec)
		print ("Average Accuracy: %0.4f" % acc)
		print ("Average FP: %0.4f" % afp)
		print ("Average FN: %0.4f" % afn)
		print ("Average TP: %0.4f" % atp)
		print ("Average TN: %0.4f" % atn)
		y_f1.append(f1)
		y_pre.append(pre)
		y_rec.append(rec)
		x.append(threshold)
		threshold += 0.01
plt.figure()
plt.plot(x, y_f1, linewidth=1)
plt.xlabel('Threshold')
plt.ylabel('F-Measure')
plt.savefig("score_threshold_curve.pdf")
plt.close()

plt.figure()
plt.plot(x, y_pre, linewidth=1)
plt.xlabel('Threshold')
plt.ylabel('Precision')
plt.savefig("precision_threshold_curve.pdf")
plt.close()

plt.figure()
plt.plot(x, y_rec, linewidth=1)
plt.xlabel('Threshold')
plt.ylabel('Recall')
plt.savefig("recall_threshold_curve.pdf")
plt.close()