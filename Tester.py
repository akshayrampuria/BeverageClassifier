import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from Trainer import Trainer
from FeatureExtractor import FeatureExtractor
from numpy import argmax
from numpy import argmin
from numpy import mean
from scipy import linalg as LA
from scipy import sparse as Sparse
import numpy
import math
from sklearn import metrics as Metrics

import numpy as np
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.learning_curve import learning_curve

class Tester:
    def __init__(self):
        self.trainer = Trainer()
        self.classifier = self.trainer.classifier
        self.testData = self.trainer.featureObj.testData
        # self.amazonData = self.trainer.featureObj.amazonData
        # self.amazonLabels = self.trainer.featureObj.amazonLabels
        # self.featureObj = FeatureExtractor(0.7)
        # self.testData = self.featureObj.testData
        # self.amazonData = self.featureObj.amazonData
        # self.amazonLabels = self.featureObj.amazonLabels
    
    def TestArray(self):
        self.prediction = []
        for i in self.testData:
            self.prediction.append(self.classifier.predict(i))
    
    def CosineSimilarity(self, x, y):
        return 1 - cosine_similarity(x, y)
        
    def GaussianDistance(self, x, y):
        return 1 - math.exp(-EuclideanDistance(x, y) ** 2)
    
    def EuclideanDistance(self, x, y):
        return euclidean_distances(x, y)
    
    def findMin(self, distVector, indices, idx):
        minVal = distVector[idx][indices[0]]
        minIdx = 0
        sumVal = 0.0
        for i in range(0, len(indices)):
            if (distVector[idx][indices[i]]) < minVal:
                minIdx = i
                minVal = distVector[idx][indices[i]]
        return minVal

    def findMax(self, distVector, indices, idx):
        maxVal = distVector[idx][indices[0]]
        maxIdx = 0
        sumVal = 0.0
        for i in range(0, len(indices)):
            if (distVector[idx][indices[i]]) > maxVal:
                maxIdx = i
                maxVal = distVector[idx][indices[i]]
        return maxVal

    def findMean(self, distVector, indices, idx):
        sumVal = 0.0
        for i in range(0, len(indices)):
            sumVal += distVector[idx][indices[i]]
        return sumVal / float(len(indices))

    def findMedian(self, distVector, indices, idx):
        sortedVector = []
        for i in range(0, len(indices)):
            sortedVector.append(distVector[idx][indices[i]])
        sortedVector.sort()
        if len(sortedVector) % 2 != 0:
            return sortedVector[len(sortedVector)/2]

        else:
            val1 = sortedVector[len(sortedVector)/2]
            val2 = sortedVector[len(sortedVector)/2 + 1]
            return (val1 + val2)/2
            
    def CreateConfusionMatrix(self, actualY):
        if hasattr(self, prediction):
            self.confMatrix = confusion_matrix(actualY, self.prediction)


    def plot_learning_curve(self,estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
        """
        Generate a simple plot of the test and traning learning curve.

        Parameters
        ----------
        estimator : object type that implements the "fit" and "predict" methods
            An object of that type which is cloned for each validation.

        title : string
            Title for the chart.

        X : array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape (n_samples) or (n_samples, n_features), optional
            Target relative to X for classification or regression;
            None for unsupervised learning.

        ylim : tuple, shape (ymin, ymax), optional
            Defines minimum and maximum yvalues plotted.

        cv : integer, cross-validation generator, optional
            If an integer is passed, it is the number of folds (defaults to 3).
            Specific cross-validation objects can be passed, see
            sklearn.cross_validation module for the list of possible objects

        n_jobs : integer, optional
            Number of jobs to run in parallel (default 1).
        """
        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")
        return plt


def main():
    T = Tester()
    # T.TestArrayIntelligently()

    y_test = T.trainer.featureObj.testLabels
    y_pred = T.prediction
    
    precision = Metrics.precision_score(y_test, y_pred, average='weighted')
    recall = Metrics.recall_score(y_test, y_pred, average='weighted')
    accuracy = Metrics.accuracy_score(y_test, y_pred)
    f1 = Metrics.f1_score(y_test, y_pred, average='weighted')
    print "Precision: ", precision
    print "Recall: ", recall
    print "Accuracy: ", accuracy
    print "F1: ", f1

    # T.plot_learning_curve(T.classifier, "Learning Curve (MultinomialNB)", T.testData, y_pred, ylim=(-2,27))

    # plt.show()
    # f1 = getF1(precision, recall)
    # print "F1 Score: ", f1
    # print(Metrics.classification_report(y_test, y_pred))
    print 'Testing complete.'

if __name__ == "__main__":
    main()
