from sklearn.metrics import f1_score

def compute_f_measure(Y_true, Y_pred):
	res = ""

	# Transform [[]] into [] :  [[0,1][1,1][0,0]] -> [0,1,1,1,0,0]
	Y_true_1d = [item for sublist in Y_true for item in sublist]
	Y_pred_1d = [item for sublist in Y_pred for item in sublist]

	ones = str(round((Y_true_1d.count(1)/len(Y_true_1d))*100, 2))
	zeros = str(round((Y_true_1d.count(0)/len(Y_true_1d))*100, 2))
	# if len(Y_true) = len(Y_pred = 1: basic validation method
	# if len(Y_true) = len(Y_pred != 1: cross validation with len(Y_true) folds
	if len(Y_true) > 1:
		res += str(len(Y_true)) + " folds cross validation | " + ones + "% 1, " +  zeros + "% 0\n"
	else:
		res += str(len(Y_true_1d)) + " test messages | " + ones + "% 1, " +  zeros + "% 0\n"
		
	res += "binary F-measure: " + str(f1_score(Y_true_1d, Y_pred_1d, average='binary', pos_label=1)) + "\n"
	res += "micro F-measure: " + str(f1_score(Y_true_1d, Y_pred_1d, average='micro', pos_label=1))  + "\n"
	res += "macro F-measure: " + str(f1_score(Y_true_1d, Y_pred_1d, average='macro', pos_label=1)) + "\n"
	res += "weighted F-measure: " + str(f1_score(Y_true_1d, Y_pred_1d, average='weighted', pos_label=1)) + "\n"
	return res