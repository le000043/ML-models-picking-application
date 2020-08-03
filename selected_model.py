import pandas as pd
import numpy as np
from sklearn import model_selection
from numpy import savetxt
import pickle
import sys
import os


selected_model = sys.argv[1]
selected_scaler = sys.argv[2]

# example of selected model name: decision_tree_classification
os.chdir('test_data')
X_test = pd.read_csv('X_test.csv')
y_test = pd.read_csv('y_test.csv')
# loading scaler
pkl_scaler_filename = selected_scaler + '_scaler.pkl'

os.chdir('../scalers')
with open (pkl_scaler_filename,'rb') as file:
  pickle_scaler = pickle.load(file)
X_test = pickle_scaler.transform(X_test) # same X-test
savetxt('X_test_copy.csv', X_test, delimiter=',')

# loading model and predicting test
os.chdir('..')
os.chdir('models')
pkl_filename = selected_model + '_model.pkl'
with open (pkl_filename,'rb') as file:
  pickle_model = pickle.load(file)
y_pred = pickle_model.predict(X_test)
print(y_pred)
os.chdir('../predictions')
savetxt('Breast_cancer_pred.csv', y_test, delimiter=',')

from sklearn.metrics import confusion_matrix, accuracy_score
accuracy = str(format(accuracy_score(y_test, y_pred),'.3f'))
print(accuracy)

