import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from FeatureExtractor import FeatureExtractor

class Trainer:
    def __init__(self):
        self.featureObj = FeatureExtractor(0.7)
        self.TrainNB()
        print "Training complete."
    
    def TrainNB(self):
        self.classifier = MultinomialNB()
        # self.classifier = RandomForestClassifier()
        # self.classifier.fit(self.featureObj.trainData.toarray(), self.featureObj.trainLabels)
        # self.classifier = SVC(probability=True)
        self.classifier.fit(self.featureObj.trainData, self.featureObj.trainLabels)

def main():
    print "Please call Tester.py"
    
if __name__ == "__main__":
    main()