from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

class F1Evaluator:

    def basic_evaluation(self, train_test_split):
        res = ""
        ones = str(round((train_test_split.true_labels.count(1)/len(train_test_split.true_labels))*100, 2))
        zeros = str(round((train_test_split.true_labels.count(0)/len(train_test_split.true_labels))*100, 2))

        res += str(len(train_test_split.true_labels)) + " test messages | " + ones + "% 1, " +  zeros + "% 0\n"
        
        res += "binary F-measure: " + str(f1_score(train_test_split.true_labels, train_test_split.predictions, average='binary', pos_label=1)) + "\n"
        res += "micro F-measure: " + str(f1_score(train_test_split.true_labels, train_test_split.predictions, average='micro', pos_label=1))  + "\n"
        res += "macro F-measure: " + str(f1_score(train_test_split.true_labels, train_test_split.predictions, average='macro', pos_label=1)) + "\n"
        res += "weighted F-measure: " + str(f1_score(train_test_split.true_labels, train_test_split.predictions, average='weighted', pos_label=1)) + "\n"
        print (res)


    def cv_evaluation(self, train_test_split):
        res = ""
        Y_true, Y_pred = [], []
        for split in train_test_split:
            Y_true.extend(split.true_labels)
            Y_pred.extend(split.predictions)

        ones = str(round((Y_true.count(1)/len(Y_true))*100, 2))
        zeros = str(round((Y_true.count(0)/len(Y_true))*100, 2))

        res += str(len(train_test_split)) + " folds cross validation | " + ones + "% 1, " +  zeros + "% 0\n"
            
        res += "binary F-measure: " + str(f1_score(Y_true, Y_pred, average='binary', pos_label=1)) + "\n"
        res += "micro F-measure: " + str(f1_score(Y_true, Y_pred, average='micro', pos_label=1))  + "\n"
        res += "macro F-measure: " + str(f1_score(Y_true, Y_pred, average='macro', pos_label=1)) + "\n"
        res += "weighted F-measure: " + str(f1_score(Y_true, Y_pred, average='weighted', pos_label=1)) + "\n"
        print (res)

        ok = 0
        fp, fn = 0, 0
        tp, tn = 0, 0
        nAbuses = 0
        for r in range(len(Y_true)):
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
        fme = 2*((pre*rec)/(pre+rec))
        print ("Average Precision: %0.4f" % pre)
        print ("Average Recall: %0.4f" % rec)
        print ("Average Accuracy: %0.4f" % acc)
        print ("Average F-measure: %s" % fme)

class AUCEvaluator:

    def basic_evaluation(self, train_test_split):
        res = ""
        ones = str(round((train_test_split.true_labels.count(1)/len(train_test_split.true_labels))*100, 2))
        zeros = str(round((train_test_split.true_labels.count(0)/len(train_test_split.true_labels))*100, 2))

        res += str(len(train_test_split.true_labels)) + " test messages | " + ones + "% 1, " +  zeros + "% 0\n"
        
        res += "micro AUC: " + str(roc_auc_score(train_test_split.true_labels, train_test_split.predictions_proba, average='micro'))  + "\n"
        res += "macro AUC: " + str(roc_auc_score(train_test_split.true_labels, train_test_split.predictions_proba, average='macro')) + "\n"
        res += "weighted AUC: " + str(roc_auc_score(train_test_split.true_labels, train_test_split.predictions_proba, average='weighted')) + "\n"
        print (res)


    def cv_evaluation(self, train_test_split):
    	print("TODO")
        #TODO