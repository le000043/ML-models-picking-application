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
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder


argsList = sys.argv
# dataset_name = argsList [2]
dataset_name = ""
"""## Importing the dataset"""
# df = pd.read_excel("Real_estate_valuation_data_set.xlsx")
# df.to_csv("Real_estate_valuation_data_set.csv", sep=",")
dataset = pd.read_csv('bank-full.csv')
X = dataset.iloc[:10, :-1].values
print(X)
ct = OneHotEncoder(handle_unknown='ignore')
transformed = ct.fit_transform(X[:, [1]]).toarray()
X = np.concatenate([X[:, :1], transformed, X[:,2:]], axis=1)

transformed = ct.fit_transform(X[:, [7]]).toarray()
X = np.concatenate([X[:, :7], transformed, X[:,8:]], axis=1)
print("TRANSFORMING...")
print(X)
# y = dataset.iloc[:, -1].values


