# -*- coding: utf-8 -*-


# Logistic Regression

## Importing the libraries

import numpy as np
from numpy import savetxt
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import path
import pickle
model_name = 'kernel_svm'
data_name = 'Breast_cancer_data'

import warnings
from warnings import simplefilter
# ignore all future warnings
"""
FutureWarning: Default solver will be changed to 'lbfgs' in 0.22. Specify a solver to silence this warning.
"""
simplefilter(action='ignore', category=FutureWarning)


"""## Training the Logistic Regression model on the Training set"""
os.chdir("train_data")
X_train = pd.read_csv('X_train.csv')
y_train = pd.read_csv('y_train.csv')
os.chdir("../test_data")
X_test = pd.read_csv('X_test.csv')
y_test = pd.read_csv('y_test.csv')

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train.values.ravel())

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
#print(cm)
def record(string,accuracy):
  return string,accuracy
accuracy = str(format(accuracy_score(y_test, y_pred),'.3f'))
# print("decision_tree: "+accuracy)
# this is to avoid the below warning
print(record("logistic_regression",accuracy))

os.chdir("../models")
pkl_model_filename = model_name + '_model.pkl'
with open (pkl_model_filename,'wb') as file:
  pickle.dump(classifier, file)
