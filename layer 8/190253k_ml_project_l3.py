# -*- coding: utf-8 -*-
"""190253K_ml_project-l3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tgnSKge9Fysam8j4mJU0hQG_MzIbD2BY
"""

# import libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# read the test and train data files
train_df = pd.read_csv("train.csv")
valid_df = pd.read_csv("valid.csv")
test_df = pd.read_csv("test.csv")

"""Label 3"""

train_3_df = train_df.iloc[:, :-1]
valid_3_df = valid_df.iloc[:, :-1]
test_3_df = test_df.iloc[:, 1:]

train_3_df.drop(columns=["label_1", "label_2"], inplace=True)
valid_3_df.drop(columns=["label_1", "label_2"], inplace=True)

train_3_df.isna().sum()

valid_3_df.isna().sum()

# splitting the test and train datasets into X and Y values
X_3_train= train_3_df.iloc[:,0:-1].values
Y_3_train = train_3_df.iloc[:,-1].values
X_3_valid = valid_3_df.iloc[:,0:-1].values
Y_3_valid = valid_3_df.iloc[:,-1].values
X_3_test = test_3_df.iloc[:,:].values

# scalling and fitting data
scaler = StandardScaler()
scaler.fit(X_3_train)

X_3_train = scaler.transform(X_3_train)
X_3_valid = scaler.transform(X_3_valid)
X_3_test = scaler.transform(X_3_test)

# compare models using cross validation
models = [RandomForestClassifier(), SVC(kernel='linear'), KNeighborsClassifier(n_neighbors=5)]

for model in models:
    cv_score = cross_val_score(model, X_3_train, Y_3_train, cv=5)
    mean_accuracy = round((sum(cv_score)/len(cv_score))*100,2)
    print("Mean accuracy % of the model: ", model, mean_accuracy)

# Use SVC since it has the highest accuracy
model = SVC(kernel='linear')
model.fit(X_3_train, Y_3_train)

y_3_valid_pred = model.predict(X_3_valid)
y_3_test_pred = model.predict(X_3_test)
print(classification_report(Y_3_valid, y_3_valid_pred))

train_3_df['label_3'].value_counts().plot(kind='bar',title='Imbalanced data')

!pip install -U imbalanced-learn

from imblearn.combine import SMOTETomek

# resampling the data

resampler = SMOTETomek(random_state=0)
X_3_train, Y_3_train = resampler.fit_resample(X_3_train, Y_3_train)

# Create a SelectKBest instance with f_classif scoring function and select top 2 features
k = 500
selector = SelectKBest(score_func=f_classif, k=k)

# Fit and transform the data
X_3_train = selector.fit_transform(X_3_train, Y_3_train)
X_3_valid = selector.transform(X_3_valid)
X_3_test = selector.transform(X_3_test)

X_3_train.shape

model.fit(X_3_train, Y_3_train)
y_3_pred_after = model.predict(X_3_valid)
print(classification_report(Y_3_valid, y_3_pred_after))

pca=PCA(0.85)
pca = pca.fit(X_3_train)

x_3_train_pca=pca.fit_transform(X_3_train)
x_3_valid_pca = pca.transform(X_3_valid)
x_3_test_pca = pca.transform(X_3_test)

# Use SVC
model.fit(x_3_train_pca, Y_3_train)

y_3_pred_after = model.predict(x_3_valid_pca)
print(classification_report(Y_3_valid, y_3_pred_after))

x_3_train_pca.shape

# Define a grid of hyperparameters to search
param_grid = {
    'C': [0.1, 1, 10],          # Regularization parameter
    'kernel': ['linear', 'rbf'],  # Kernel type
    'gamma': ['scale', 'auto']   # Kernel coefficient for 'rbf' kernel
}

# Create a GridSearchCV object with cross-validation (e.g., 5-fold cross-validation)
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')

# Fit the GridSearchCV instance to the training data
grid_search.fit(x_3_train_pca, Y_3_train)

# Get the best hyperparameters and model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Evaluate the best model on the test set
y_3_pred_after = best_model.predict(x_3_valid_pca)
preds = best_model.predict(x_3_test_pca)

print("Best Hyperparameters:", best_params)
print(classification_report(Y_3_valid, y_3_pred_after))

data_frame = pd.DataFrame(preds, columns=["label_3"])
data_frame.to_csv(f"190253K_3.csv",na_rep='')

