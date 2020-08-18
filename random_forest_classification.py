# -*- coding: utf-8 -*-


# Random Forest Classification

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


"""## Training the Random Forest Classification model on the Training set"""
os.chdir("train_data")
X_train = pd.read_csv('X_train.csv')
y_train = pd.read_csv('y_train.csv')
os.chdir("../test_data")
X_test = pd.read_csv('X_test.csv')
y_test = pd.read_csv('y_test.csv')

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
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
print(record("random_forest_classification",accuracy))

os.chdir("../models")
pkl_model_filename = model_name + '_model.pkl'
with open (pkl_model_filename,'wb') as file:
  pickle.dump(classifier, file)