# -*- coding: utf-8 -*-
# Support Vector Machine (SVM)
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

"""## Importing the dataset"""

dataset = pd.read_csv('Breast_cancer_data.csv')
X = dataset.iloc[:, :-1].values.astype(float)
y = dataset.iloc[:, -1].values.astype(float)

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

"""## Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Training the SVM model on the Training set"""

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
#print(cm)

def record(string,accuracy):
  return string,accuracy
accuracy = str(format(accuracy_score(y_test, y_pred),'.3f'))
# print("decision_tree: "+accuracy)
print(record("support_vector_machine",accuracy))

os.chdir("models")
pkl_model_filename = model_name + '_model.pkl'
with open (pkl_model_filename,'wb') as file:
  pickle.dump(classifier, file)