#%%
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the data
testdata = pd.read_csv('X.csv')
data = pd.read_csv('formatted_data.csv')

# drop any rows with missing values

data = data.dropna()

# Split the data into training and test sets
y= data['final_weight_grams']
X = data.drop(columns=['final_weight_grams'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#%%
# train the model

model = LinearRegression()

model.fit(X_train, y_train)

model.coef_

#%%
# test the model
y_pred = model.predict(X_train)

y_pred



#print(data)
# %%
