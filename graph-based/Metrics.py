from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score

class F1Evaluator:

    def evaluate(self, classifier):
        """Evaluates the classification performances in terms of F-measure. Prints the results.

        Args:
         classifier: The classifier used to perform the classification.

        """
        res = ""
        # Proportions of abusive and non-abusive messages in the test split
        ones = str(round((classifier.Y_true.count(1)/len(classifier.Y_true))*100, 2))
        zeros = str(round((classifier.Y_true.count(0)/len(classifier.Y_true))*100, 2))

        res += str(len(classifier.Y_true)) + " test messages | " + ones + "% 1, " +  zeros + "% 0\n"
        
        res += "binary F-measure: " + str(f1_score(classifier.Y_true, classifier.predictions, average='binary', pos_label=1)) + "\n"
        res += "micro F-measure: " + str(f1_score(classifier.Y_true, classifier.predictions, average='micro', pos_label=1))  + "\n"
        res += "macro F-measure: " + str(f1_score(classifier.Y_true, classifier.predictions, average='macro', pos_label=1)) + "\n"
        res += "weighted F-measure: " + str(f1_score(classifier.Y_true, classifier.predictions, average='weighted', pos_label=1)) + "\n"
        print (res)
