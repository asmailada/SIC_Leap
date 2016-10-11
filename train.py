import sys
import os
import numpy as np
import pylab as pl
import glob
import cv2
import subprocess
import time
import math
import re
import pickle
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

def tune(samples, labels):
	# Split the dataset in two equal parts
	X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size = 0.5, random_state = 0)

	# Set the parameters by cross-validation
	tuned_parameters = [{'kernel': ['rbf'], 'gamma': np.logspace(-6.0, 3.0, num = 20).tolist(), 'C': np.logspace(-2.0, 3.0, num = 20).tolist()}]

	scores = ['precision', 'recall']

	for score in scores:
	    print("# Tuning hyper-parameters for %s" % score)

	    clf = GridSearchCV(SVC(C = 1), tuned_parameters, cv = 5, scoring='%s_weighted' % score)
	    clf.fit(X_train, y_train)

	    print("Best parameters set found on development set:")
	    print(clf.best_params_)
	    print("Grid scores on development set:")
	    for params, mean_score, scores in clf.grid_scores_:
	        print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))

	    print "Detailed classification report:"
	    print "The model is trained on the full development set."
	    print "The scores are computed on the full evaluation set."
	    y_true, y_pred = y_test, clf.predict(X_test)
	    print classification_report(y_true, y_pred)

def SVM(samples, labels, argv):
	print "building SVM model..."
	c = 297.63514416313194
	gamma = 0.01832980710832434
	svc = SVC(kernel = 'rbf', C = c, gamma = gamma) 
	svc.fit(samples, labels)
	joblib.dump(svc, 'model.pkl') 

def train_SVM(argv,isTune):
	samples = []
	labels = []
	for i in range(0,len(argv)-2):
		print argv[i+2]
		dumpfile = open(argv[i+2],"r")
		num = 0
		while True:
			try:
				samples.insert(0,pickle.load(dumpfile))
				labels.insert(0,i%3)
				num += 1
			except EOFError:
				break
			if num >= 1300:
				break
		print num
	print len(samples)
	SVM(samples, labels, argv)
	if isTune == 1:
		tune(samples, labels)

def test_SVM(testing):
	enumm = dict({0:"paper",1:"scissor",2:"stone"})
	svc = joblib.load('model.pkl')
	testingdata = []
	testingfile = open(testing,"r")
	num = 0
	while True:
		try:
			testingdata.insert(0,pickle.load(testingfile))
			num += 1
		except EOFError:
			break
	print testing
	print len(testingdata)
	print "Predict: ",[enumm[i] for i in svc.predict(testingdata)]

if __name__ == '__main__':
	if (sys.argv[1]=="--train"):
		train_SVM(sys.argv,0)
	if (sys.argv[1]=="--tune"):
		train_SVM(sys.argv,1)
	if (sys.argv[1]=="--test"):
		test_SVM(sys.argv[2])

