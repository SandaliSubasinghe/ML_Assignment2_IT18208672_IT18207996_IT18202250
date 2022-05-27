# -*- coding: utf-8 -*-
"""LogisticRegression-FakeNewsPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at :
    https://colab.research.google.com/drive/1OOxFm9jB_RzRS-UqlNVVLy7QLagiU6t_?usp=sharing
    

## **Import Required Innitial Dependencies**
"""

import numpy as np
import pandas as pd

"""## **Load the training datasets**"""

train_data = pd.read_csv('/content/train.csv')

train_data.head()

print(train_data.shape)

"""# **Data Pre-processing**

Check for null values and replace the null values with empty string
"""

# Check for null values of train data set
train_data.isnull().sum()

# Replace the null value with empty string in train data
train_data = train_data.fillna('')

# After replacing the null values with empty string in train data
train_data.isnull().sum()

"""Identify the stopwords"""

# Import stopwords
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')

# Print stopwords
print(stopwords.words('english'))

"""Merge the author column and title colum"""

# Merge the author column and title colum in train dataset
train_data['merged_title_and_author'] = train_data['author']+[' ']+train_data['title']

print(train_data['merged_title_and_author'])

"""## **Seperating indipendent and dependent variables**"""

# Removing label column from training data set
X = train_data.drop(columns='label', axis=1)

print(X)

# Store label in Y variable 
Y = train_data['label']

print(Y)

"""## **Stemming**"""

# Import dependences for stemming
from nltk.stem.porter import PorterStemmer

import re

porter_stemmer = PorterStemmer()

def stemmimg(data):
  remove_unnecessary_charactors = re.sub('[^a-zA-Z]', ' ', data)
  to_lowercase = remove_unnecessary_charactors.lower()
  splitting = to_lowercase.split()
  stemming_data = [porter_stemmer.stem(word) for word in splitting if not word in stopwords.words('english')]
  final_data = ' '.join(stemming_data)

  return final_data

train_data['merged_title_and_author'] = train_data['merged_title_and_author'].apply(stemmimg)

print(train_data['merged_title_and_author'])

"""## **Seperating the indipendent and dependent variables after stemming**"""

new_X = train_data['merged_title_and_author'].values
new_Y = train_data['label'].values

print(new_X)

print(new_Y)

"""## **Convert text into numarical data**"""

# Import dependences to convert text into numarical form
from sklearn.feature_extraction.text import TfidfVectorizer

tf_idf_vectorizer = TfidfVectorizer()
tf_idf_vectorizer.fit(new_X)

new_X = tf_idf_vectorizer.transform(new_X)

print(new_X)

"""## **Splitting dataset to training and test data**"""

# Import dependencies to split train and test data
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(new_X, new_Y, test_size = 0.2, stratify=new_Y, random_state=4)

"""# **Training the model**"""

# Import dependencies of logistic regression
from sklearn.linear_model import LogisticRegression

logistic_regression_model = LogisticRegression()

#Train the model
logistic_regression_model.fit(X_train, Y_train)

"""## **Check the Accuracy**"""

# Import the dependency required to check the accuracy
from sklearn.metrics import accuracy_score

# Check the accurscy score of train data
prediction_of_X_train = logistic_regression_model.predict(X_train)
X_train_accuraccy = accuracy_score(prediction_of_X_train, Y_train)

print('Accuracy score of logistic regression train data : ', X_train_accuraccy)

# Check the accurscy score of test data
prediction_of_X_test = logistic_regression_model.predict(X_test)
X_test_accuraccy = accuracy_score(prediction_of_X_test, Y_test)

print('Accuracy score of logistic regression test data : ', X_test_accuraccy)

"""## **Confusion Matrix**"""

# Import required libraries
import matplotlib.pyplot as plt
from sklearn import metrics
import itertools

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion Matrix - Logistic Regression', cmap=plt.cm.Greens):
  plt.imshow(cm, interpolation='nearest', cmap=cmap)
  plt.title(title)
  plt.colorbar()
  tick_marks = np.arange(len(classes))
  plt.xticks(tick_marks, classes, rotation=45)
  plt.yticks(tick_marks, classes)

  if normalize:
    confusion_matrix = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print("Normalized confusion matrix")
  else:
      print('Confusion matrix, without normalization')
  thresh = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
      plt.text(j, i, cm[i, j],horizontalalignment="center",color="white" if cm[i, j] > thresh else "black")

  plt.tight_layout()
  plt.ylabel('True label')
  plt.xlabel('Predicted label')

confusion_matrix_logistic = metrics.confusion_matrix(prediction_of_X_test, Y_test)
plot_confusion_matrix(confusion_matrix_logistic, classes=['FAKE NEWS', 'REAL NEWS'])

"""## **Test Prediction**"""

X_value = X_test[5]

prediction = logistic_regression_model.predict(X_value)
print(prediction)

if(prediction[0]==0):
  print('The news is a real news')

else:
  print('The news is a fake news')

# Check the label
print(Y_test[5])