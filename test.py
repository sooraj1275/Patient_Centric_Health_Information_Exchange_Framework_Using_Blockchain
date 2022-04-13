import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the datasets
feat_labels = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']


datasets = pd.read_csv(r'D:\backups\HDP Riya richu\heart\static\heart.xls')
X = datasets.iloc[:,0:13].values
Y = datasets.iloc[:, 13].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=0)


clf = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)

#lk Train the classifier
clf.fit(X_train, y_train)

#lk Print the name and gini importance of each feature
# for feature in zip(feat_labels, clf.feature_importances_):
#     print(feature)



sfm = SelectFromModel(clf, threshold=0.1)

sfm.fit(X_train, y_train)

X_important_train = sfm.transform(X_train)
X_important_test = sfm.transform(X_test)

# print(X_important_test)



#
clf_important = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
#
# # Train the new classifier on the new dataset containing the most important features
clf_important.fit(X_important_train, y_train)
# print("trained")
#
# y_pred = clf.predict(X_important_test)
# print("predicted")
# # View The Accuracy Of Our Full Feature (4 Features) Model
# s=accuracy_score(y_test, y_pred)
#
# print(s)