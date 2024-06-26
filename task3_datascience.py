# -*- coding: utf-8 -*-
"""Task3 DataScience.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13jeoscWt0PQIyvPAC4ZBAuAXkrvTOsKS

# **Email Spam Filtering Task**

# **Important Libraries**
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/content/spam.csv",encoding='latin-1')
df

df.shape

df.info()

df.duplicated().sum()

df=df.drop_duplicates(keep='first')

columns_to_drop = ["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"]
df.drop(columns=columns_to_drop, inplace=True)

df.shape

new_column_names = {"v1":"Category","v2":"Message"}
df.rename(columns = new_column_names,inplace = True)

df.isnull().sum()

#Secondly, I plot the 30 most common words within those categories.
ham_ct  = Counter(" ".join(df[df['Category']=='ham']["Message"]).split()).most_common(30)
spam_ct = Counter(" ".join(df[df['Category']=='spam']["Message"]).split()).most_common(30)

df_ham = pd.DataFrame.from_dict(ham_ct)
df_ham = df_ham.rename(columns={0: "word", 1 : "count"})
df_spam = pd.DataFrame.from_dict(spam_ct)
df_spam = df_spam.rename(columns={0: "word", 1 : "count"})

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
df_ham.plot.bar(x='word', y='count', legend=False, ax=axes[0])
df_spam.plot.bar(x='word', y='count', color='red', legend=False, ax=axes[1])

axes[0].set_title('Non-Spam')
axes[1].set_title('Spam')

plt.show()

data = df.where((pd.notnull(df)), ' ')

data.head(10)

data.describe()

data.loc[data["Category"] == "spam", "Category"] = 0
data.loc[data["Category"] == "ham", "Category"] = 1

data

# Separate the feature (message) and target (category) data
X = data["Message"]
Y = data["Category"]

X

Y

#Split the data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 3)

print(X.shape)
print(X_train.shape)
print(X_test.shape)

# Create a TF-IDF vectorizer to convert text messages into numerical features

feature_extraction = TfidfVectorizer(min_df=1, stop_words="english", lowercase=True)

# Convert the training and testing text messages into numerical features using TF-IDF

X_train_features = feature_extraction.fit_transform(X_train)
X_test_features = feature_extraction.transform(X_test)

# Convert the target values to integers (0 and 1)

Y_train = Y_train.astype("int")
Y_test = Y_test.astype("int")

# Data visualization - Distribution of Spam and Ham Emails

spam_count = data[data['Category'] == 0].shape[0]
ham_count = data[data['Category'] == 1].shape[0]

plt.bar(['Spam', 'Ham'], [spam_count, ham_count])
plt.xlabel('Email Type')
plt.ylabel('Count')
plt.title('Distribution of Spam and Ham Emails')
plt.show()

"""# **Logistic Regression with Accuracy 96%**"""

model = LogisticRegression()
model.fit(X_train_features, Y_train)
# Make predictions on the training data and calculate the accuracy

prediction_on_training_data = model.predict(X_train_features)
accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)
print("Accuracy on training data:",accuracy_on_training_data)
# Make predictions on the test data and calculate the accuracy

prediction_on_test_data = model.predict(X_test_features)
accuracy_on_test_data = accuracy_score(Y_test,prediction_on_test_data)
print("Accuracy on test data:",accuracy_on_test_data)

"""# **Decision Tree with Accuracy 93.3%**"""

dtc = DecisionTreeClassifier(max_depth=5)

dtc.fit(X_train_features, Y_train)
# Make predictions on the training data and calculate the accuracy

predict_on_training_data = dtc.predict(X_train_features)
accuracy_training_data = accuracy_score(Y_train, predict_on_training_data)

print("Accuracy on training data:",accuracy_training_data)
# Make predictions on the test data and calculate the accuracy

predict_on_test_data = dtc.predict(X_test_features)
accuracy_test_data = accuracy_score(Y_test,predict_on_test_data)
print("Accuracy on test data:",accuracy_test_data)

"""# **Gradient Boosting with Accuracy 95%**"""

gbdt = GradientBoostingClassifier(n_estimators=50,random_state=2)
gbdt.fit(X_train_features, Y_train)
# Make predictions on the training data and calculate the accuracy

training_data = gbdt.predict(X_train_features)
accuracy_training = accuracy_score(Y_train,training_data)

print("Accuracy on training data:",accuracy_training)
# Make predictions on the test data and calculate the accuracy

test_data = gbdt.predict(X_test_features)
accu_test_data = accuracy_score(Y_test,test_data)
print("Accuracy on test data:",accu_test_data)

"""# **Random Forest with Accuracy 97%**"""

rfc = RandomForestClassifier(n_estimators=50, random_state=2)
rfc.fit(X_train_features, Y_train)

training_dat = rfc.predict(X_train_features)
accuracy_train = accuracy_score(Y_train,training_dat)

print("Accuracy on training data:",accuracy_train)

test_data = rfc.predict(X_test_features)
acc_test_data = accuracy_score(Y_test,test_data)
print("Accuracy on test data:",acc_test_data)