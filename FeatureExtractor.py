import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from collections import Counter
from DataReader import DataReader
import numpy as np
from scipy.sparse import csr_matrix
import random
import ast

class FeatureExtractor:
    
    def ProcessTokens(self, tokens):
        tokens = tokens.split()
        newTokens = []
        for token in tokens:
            if ((token[:4] != '.') and (token != '!')):
                newTokens.append(token)
        return ' '.join(newTokens)
    
   # Creates term count vectors for each user
    def CreateTermCountVector(self):
        self.corpus = []
        self.trainList = []
        self.trainLabels = []
        self.testList = []
        self.testLabels = []
        for key in self.documentMap:
            docList = self.documentMap[key]
            for i in range(0, len(docList)):
                tokens = docList[i]
                # Make lowercase, remove punctuation and tokenize
                tokens = tokens.lower()
                # tokens = self.ProcessTokens(tokens)
                tokens = tokens.translate(None, string.punctuation)
                tokens = tokens.split()
                # Remove stop words like 'the', 'i' etc
                filteredTokens = [word for word in tokens if not word in stopwords.words('english')]
                docList[i] = ' '.join(filteredTokens)
            self.documentMap[key] = docList
            k = int(self.percentage*len(docList))
            for i in range(0, k):
                self.trainList.append(docList[i])
                self.corpus.append(docList[i])
                self.trainLabels.append(key)
            for i in range(k, len(docList)):
                self.testList.append(docList[i])
                self.testLabels.append(key)

    
    def CreateVocabulary(self):
        self.vocabulary = []
        for i in self.corpus:
            for j in i.split():
                self.vocabulary.append(j)
            self.vocabulary = list(set(self.vocabulary))
        print len(self.vocabulary)

    def saveTFIDF(self, filename, array):
        np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

    def load_sparse(self, filename):
        loader = np.load(filename)
        return csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])
    
    def CalculateTFIDF(self):
        self.tfidfVectorizer = TfidfVectorizer(smooth_idf=True, vocabulary=self.vocabulary, sublinear_tf=True, norm='l2')
        self.trainData = self.tfidfVectorizer.fit_transform(self.trainList)
        self.testData = self.tfidfVectorizer.fit_transform(self.testList)
        # self.featureNames = self.tfidfVectorizer.get_feature_names()
        
    def __init__(self, percentage):
        self.percentage = percentage

        self.dataObj = DataReader()
        # self.documentMap = self.dataObj.socialMap
        self.CreateTermCountVector()
        self.CreateVocabulary()
        self.CalculateTFIDF()
        
        # self.trainData = self.load_sparse("socialtrain.npz")
        # self.testData = self.load_sparse("socialtest.npz")
        
        print 'Loaded feature vectors.'
        
        # self.trainLabels = 
            
        # self.testLabels = 
            
        # self.corpus = 

        self.numDocuments = len(self.corpus)
        
def main():
    print "Please call Tester.py"
    
if __name__ == "__main__":
    main()