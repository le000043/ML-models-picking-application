# -*- coding: utf-8 -*-

# Decision Tree Classification

## Importing the libraries
import numpy as np
from numpy import savetxt
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import path
import pickle
import sys

argsList = sys.argv
dataset_name = ""
"""## Importing the dataset"""

# dataset = pd.read_csv('Breast_cancer_data.csv')
# X = dataset.iloc[:, :-1].values.astype(float)
# y = dataset.iloc[:, -1].values.astype(float)

# saving clean data
# savetxt('clean_X_data.csv', X, delimiter=',')
# savetxt('clean_y_data.csv', y, delimiter=',')


"""## Splitting the dataset into the Training set and Test set"""

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
# os.chdir("test_data")
# csvFile01 = open('X_test.csv','w')

# current_path = os.path.dirname('test_data') 
# csvFile02 = open('y_test.csv','w')

# column = "N/A"
# for i in range (len(X[0])-1):
#   column += ", N/A"

# savetxt(csvFile01, X_test, delimiter=',', header = column)
# savetxt(csvFile02, y_test, delimiter=',', header = column[0])
"""## Feature Scaling"""

# from sklearn.preprocessing import StandardScaler
# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)

# os.chdir("../scalers")
# pkl_scaler_filename = 'breast_cancer_data_scaler.pkl'
# with open (pkl_scaler_filename,'wb') as file:
#   pickle.dump(sc, file)

# X_test = sc.transform(X_test)


"""## Training the Decision Tree Classification model on the Training set"""
os.chdir("train_data")
X_train = pd.read_csv('X_train.csv')
y_train = pd.read_csv('y_train.csv')

os.chdir("../test_data")
X_test = pd.read_csv('X_test.csv')
y_test = pd.read_csv('y_test.csv')

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
#print(cm)
def record(string,accuracy):
  return string,accuracy
accuracy = str(format(accuracy_score(y_test, y_pred),'.3f'))
# savetxt('y_pred_original.csv', y_test, delimiter=',')
print(record("decision_tree_classification",accuracy))
# print(y_pred)
# saving the model and scaler for later use

os.chdir("../models")
pkl_model_filename = 'decision_tree_classification'+dataset_name+'_model.pkl'
with open (pkl_model_filename,'wb') as file:
  pickle.dump(classifier, file)

# csvFile01.close()
# csvFile02.close()
