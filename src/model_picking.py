import pandas as pd
import numpy as np
from sklearn import model_selection
from numpy import savetxt
import pickle
import sys
import os

argsList = sys.argv

input_dataset_name = argsList[1][:-4]
test_dataset_name = argsList[2]
# output_name = argsList[3]

print("input_dataset_name: "+str(input_dataset_name))
print("test_dataset_name: "+str(test_dataset_name))
# print("output_name: "+str(output_name))


def sanitize(name, accuracy):
  name = name[2:]
  name = name[:-1]
  accuracy = accuracy [2:]
  accuracy = accuracy [:-3]
  return name,accuracy
file1 = open('output.txt', 'r')
best_accuracy = 0
best_algo = ""
count = 0
arr = []
while True:
    count += 1
    line = file1.readline()
    if not line:
      break
    comma_index = line.index(',')
    name, accuracy = sanitize (line[:comma_index], line[comma_index+1:])

    arr.append({name:accuracy})
    accuracy = float (accuracy)
    if accuracy > best_accuracy:
      best_accuracy = accuracy
      best_algo = name

file1.close()



# print("best_accuracy: " + str(format((best_accuracy * 100),'.2f')+" %"))
# print("best_algo: " + best_algo)

# selected_model = sys.argv[1]
selected_model = best_algo
# selected_scaler = sys.argv[2]
selected_scaler = input_dataset_name

# example of selected model name: decision_tree_classification
os.chdir('test_data')
# X_test = pd.read_csv('X_test.csv')
real_test = pd.read_csv(test_dataset_name)
y_test = pd.read_csv('y_test.csv')
# loading scaler
pkl_scaler_filename = selected_scaler + '_scaler.pkl'

# loading model and predicting test
os.chdir('..')
os.chdir('models')
pkl_filename = selected_model + '_model.pkl'

with open (pkl_filename,'rb') as file:
  pickle_model = pickle.load(file)
y_pred = pickle_model.predict(real_test)

# print(type(y_pred))
# print("result matrix:")
# print(y_pred)

# write prediction to a csv file

os.chdir('../predictions')
output_name = input_dataset_name +"_prediction_"+ '.csv'
savetxt(output_name, y_pred, delimiter=',')
print("FINISH SAVING PREDICTION TO FILE "+output_name + " in prediction folder")
from sklearn.metrics import confusion_matrix, accuracy_score
accuracy = str(format(accuracy_score(y_test, y_pred),'.3f'))
