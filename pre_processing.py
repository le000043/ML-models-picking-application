import numpy as np
from numpy import savetxt
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import path
import pickle
import sys

argsList = sys.argv     # arguments from C script

data_name = argsList[1]
dataset = pd.read_csv(data_name)
X = dataset.iloc[:, :-1].values.astype(float)
y = dataset.iloc[:, -1].values.astype(float)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# column = "N/A"
# for i in range (len(X[0])-1):
#   column += ", N/A"

# os.chdir("train_data")
# csvFile01 = open('X_train.csv','w')
# savetxt(csvFile01, X_train, delimiter=',')
# csvFile02 = open('y_train.csv','w')
# savetxt(csvFile02, y_train, delimiter=',')

# os.chdir("../test_data")
# csvFile03 = open('X_test.csv','w')
# current_path = os.path.dirname('test_data') 
# csvFile04 = open('y_test.csv','w')
# savetxt(csvFile03, X_test, delimiter=',', header = column)
# savetxt(csvFile04, y_test, delimiter=',', header = column[0])
"""## Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
os.chdir("scalers")
pkl_scaler_filename = 'breast_cancer_data_scaler.pkl'
with open (pkl_scaler_filename,'wb') as file:
  pickle.dump(sc, file)

X_test = sc.transform(X_test)

column = "N/A"
for i in range (len(X[0])-1):
  column += ", N/A"

os.chdir("../train_data")
csvFile01 = open('X_train.csv','w')
savetxt(csvFile01, X_train, delimiter=',')
csvFile02 = open('y_train.csv','w')
savetxt(csvFile02, y_train, delimiter=',')

os.chdir("../test_data")
csvFile03 = open('X_test.csv','w')
current_path = os.path.dirname('test_data') 
csvFile04 = open('y_test.csv','w')
savetxt(csvFile03, X_test, delimiter=',', header = column)
savetxt(csvFile04, y_test, delimiter=',', header = column[0])
csvFile01.close()
csvFile02.close()
csvFile03.close()
csvFile04.close()

