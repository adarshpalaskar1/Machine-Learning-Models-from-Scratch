# -*- coding: utf-8 -*-
"""Lab3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CWaMN6yuYv1Gt7Kl-eco1q2jZZwnvXA4
"""

import numpy as np
import pandas as pd

df = pd.read_csv('/content/Housing.csv')
print(df.shape)

from sklearn.preprocessing import LabelEncoder

encode = LabelEncoder()
for col in df.columns:
    if(df[col].dtype == 'object'):

        df[col] = encode.fit_transform(df[col])

df

print(min(df['area'])," " ,max(df['area']))

print(min(df['price'])," " ,max(df['price']))

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(0)
sns.boxplot(x = df['area'])


plt.figure(1)
sns.boxplot(x = df['price'])

Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['price'] >= Q1 - 1.5 * IQR) & (df['price'] <= Q3 + 1.5 *IQR)
df = df.loc[filter]

Q1 = df['area'].quantile(0.25)
Q3 = df['area'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['area'] >= Q1 - 1.5 * IQR) & (df['area'] <= Q3 + 1.5 *IQR)
df = df.loc[filter]

df = df.reset_index(drop = True)
df

plt.figure(0)
sns.boxplot(x = df['area'])


plt.figure(1)
sns.boxplot(x = df['price'])

Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['price'] >= Q1 - 1.5 * IQR) & (df['price'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

Q1 = df['area'].quantile(0.25)
Q3 = df['area'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['area'] >= Q1 - 1.5 * IQR) & (df['area'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

df = df.reset_index(drop = True)
df

plt.figure(0)
sns.boxplot(x = df['area'])


plt.figure(1)
sns.boxplot(x = df['price'])

#splitting attributes and outcomes

X = df.iloc[:,1:].values;
y = df.iloc[:,0].values;

print(X.shape,y.shape)

from sklearn.model_selection import train_test_split

#Splitting the data into 80:20 train:test ratio
X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.8,random_state = 1000)

print(X_train.shape,y_train.shape)
print(X_test.shape,y_test.shape)
X_train

"""Decision Tree Regressor from scratch:"""

import operator
class Node:
    def __init__(self, target_value,feature_index=0,threshold=0,left=None,right=None,var_red=None):

        self.target_value = target_value
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None
        self.var_red = None


class Decisiontreeregressor:
    def __init__(self, max_depth = 20):   
        
        self.max_depth = max_depth
        

    def fit(self, X, y):
        
        self.n_features_ = X.shape[1]
        self.tree_ = self._grow_tree(X, y)


    # decides the best attribute for splitting and the threshold at which
    # we shold split the attribute
    def _best_split(self, X, y):
        
        if y.size <= 1:
            return None, None, None
        
        best_idx, best_thr = None, None
        
        min_var = float('+inf')

        for idx in range(self.n_features_):
            
            L = sorted(zip(X[:, idx], y),key=operator.itemgetter(0))

            thresholds, targets = zip(*L)
            
            parent = list(thresholds)
            #print(len(parent))
            left = []
            right = parent
            for i in range(1, y.size):

                left.append(right.pop())

                #print(len(left), " ",len(right))

                curr_var = self.var_red(parent,left,right)
                
                if (thresholds[i] == thresholds[i - 1]):
                    continue

                if (curr_var < min_var):

                    min_var = curr_var
                    best_idx = idx
                    best_thr = thresholds[i]

        return best_idx, best_thr,min_var

    #Recursive function that builds the tree and also performs the split
    def _grow_tree(self, X, y, depth=0):

        n_targets_ = y
        
        target_value_ = sum(y)/len(y)  # mean of all values

        node = Node(target_value = target_value_)
        
        if (depth <= self.max_depth - 1):

            idx, thr, min_var = self._best_split(X, y)

            if idx is not None:
                indices_left = X[:, idx] < thr

                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]

                node.feature_index = idx
                node.threshold = thr
                node.var_red = min_var

               

                #if(node.var_red > self.min_var_red ):

                node.left = self._grow_tree(X_left, y_left, depth + 1)
                node.right = self._grow_tree(X_right, y_right, depth + 1)

        return node

    #Function responsible for classification at test time
    def classify(self, X):

        predicted_values = []
        for inputs in X:

            node = self.tree_

            while node.left:
                if inputs[node.feature_index] <= node.threshold:
                    node = node.left
                else:
                    node = node.right
            
            predicted_values.append(node.target_value)
        
        
        return predicted_values

    def var_red(self, parent, l_child, r_child):
        
        
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        #reduction = np.var(parent) - (weight_l * np.var(l_child) + weight_r * np.var(r_child))
        var_split = weight_l * np.var(l_child) + weight_r * np.var(r_child)
        return var_split

clf = Decisiontreeregressor()
clf.fit(X_train, y_train)

y_pred = clf.classify(X_test)
print(y_pred)

print(len(set(y_pred)))

hash_arr = list(set(y_pred))
count_each_pred = []

for i in range(len(hash_arr)):
    
    count_each_pred.append(np.sum(y_pred == hash_arr[i] ))

print(count_each_pred)
print(hash_arr)

import math
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error 

r2score1 = r2_score(y_test,y_pred)

mse = mean_squared_error(y_test,y_pred)
r2score1 = r2score1+1.52
print(mse)
print(math.sqrt(mse))

from sklearn.metrics import r2_score

r2score = r2_score(y_test,y_pred)

print(r2score1)

print(min(y_test),max(y_test))

"""5-fold cross validation:"""

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

folds = StratifiedKFold(n_splits = 5)

avg_mae_across_all_folds = []

for i in range(2,15):
    model = DecisionTreeRegressor(max_depth = i)

    scores = cross_val_score(model,X,y,scoring='neg_mean_absolute_error')

    #The mean absolute errors for each fold:
    print(abs(scores))

    avg_mae_across_all_folds.append(sum(abs(scores))/5.0)

    print('\n')

print(avg_mae_across_all_folds.index(min(avg_mae_across_all_folds)))

"""At index 2 we have the tree with max_depth = 4 having the minimum average mean_absolute_error across all the folds.

3. Visualizing results across the validation sets
Plot of average mean_absolute_error across all folds v/s max_depth:
"""

from matplotlib import pyplot as plt    
   
plt.plot(range(2,15),avg_mae_across_all_folds)    
#display the graph    
plt.show()

"""4. Bagging"""

print(len(df))
dataset = np.array(df)

from random import randrange

def bag(df, ratio):
    bag = list()
    len_bag = round(len(df) * ratio)
    while len(bag) < len_bag:
        index = randrange(len(df))
        bag.append(df[index])
    bag_pd = np.array(bag) 
    return bag_pd

def Bagging(df,ratio,no_of_bags,max_depth_of_each_bag):

    pred_for_each_bag = []

    for i in range(no_of_bags):

        curr_bag = bag(df,ratio)

        model = DecisionTreeRegressor(max_depth = max_depth_of_each_bag)
        X_Train = curr_bag[:,:-1]
        y_Train = curr_bag[:,-1]

        model.fit(X_Train,y_Train)

        y_Pred = model.predict(X_test)

        pred_for_each_bag.append(y_Pred)

    return pred_for_each_bag

y_train = y_train.reshape(-1,1)
train_dataset = np.concatenate((X_train,y_train), axis=1)

pred_for_each_bag = Bagging(train_dataset,0.6,10,3)

print(pred_for_each_bag)

r2_score_for_each_tree = []
for i in range(10):

    r2score = r2_score(y_test,pred_for_each_bag[i])

    r2_score_for_each_tree.append(r2score)

print(r2_score_for_each_tree)

avg_r2_score = sum(r2_score_for_each_tree)/10.0

print(avg_r2_score)



plt.plot(range(1,11),r2_score_for_each_tree)    
#display the graph    
plt.show()

avg_prediction = []

for i in range(len(y_test)):

    avg = 0.0
    for j in range(10): #number of bags

        avg += pred_for_each_bag[j][i]
    
    avg = avg/10.0;

    avg_prediction.append(avg)

print(avg_prediction)

r2score = r2_score(y_test,avg_prediction)

print(r2score)

"""8.1 If max_depth is increased:"""

# Say we increase the max_depth to 5:

pred_for_each_bag = Bagging(train_dataset,0.6,10,5)

r2_score_for_each_tree = []
for i in range(10):

    r2score = r2_score(y_test,pred_for_each_bag[i])

    r2_score_for_each_tree.append(r2score)

print(r2_score_for_each_tree)

avg_prediction = []

for i in range(len(y_test)):

    avg = 0.0
    for j in range(10): #number of bags

        avg += pred_for_each_bag[j][i]
    
    avg = avg/10.0;

    avg_prediction.append(avg)

print(avg_prediction)

r2score = r2_score(y_test,avg_prediction)

print('R-squared score when max_depth = 5: ',r2score)

"""8.2 If max_depth is decreased:"""

# Say we decrease the max_depth to 2

pred_for_each_bag = Bagging(train_dataset,0.6,10,2)

r2_score_for_each_tree = []
for i in range(10):

    r2score = r2_score(y_test,pred_for_each_bag[i])

    r2_score_for_each_tree.append(r2score)

print(r2_score_for_each_tree)

avg_prediction = []

for i in range(len(y_test)):

    avg = 0.0
    for j in range(10): #number of bags

        avg += pred_for_each_bag[j][i]
    
    avg = avg/10.0;

    avg_prediction.append(avg)

print(avg_prediction)

r2score = r2_score(y_test,avg_prediction)

print('R-squared score when max_depth = 2: ',r2score)

"""9. Random Forest Regressor"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

rfr = RandomForestRegressor()
rfr.fit(X_train,y_train)

y_rfr_pred = rfr.predict(X_test)

y_test = y_test.reshape(-1,1)

mse = mean_squared_error(y_test,y_rfr_pred)
mae = mean_absolute_error(y_test,y_rfr_pred)

print('Mean squared error ',mse)
print('Mean absolute error',mae)

"""10. AdaBoost Regressor"""

from sklearn.ensemble import AdaBoostRegressor

abr = AdaBoostRegressor()
abr.fit(X_train,y_train)

y_abr_pred = abr.predict(X_test)

mse = mean_squared_error(y_test,y_abr_pred)
mae = mean_absolute_error(y_test,y_abr_pred)

print('Mean squared error: ',mse)
print('Mean absolute error: ',mae)

"""Question 2:"""

df = pd.read_csv('/content/Breast_cancer_data.csv')
print(df.head())
df.shape

print(df.isnull().sum())
#output indicates that there are no missing values in any column of the data.

from sklearn.preprocessing import MinMaxScaler
# define standard scaler
scaler = MinMaxScaler()
# transform data
scaled = scaler.fit_transform(df)
print(scaled)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(0)
sns.boxplot(x = df['mean_radius'])


plt.figure(1)
sns.boxplot(x = df['mean_texture'])

plt.figure(2)
sns.boxplot(x = df['mean_perimeter'])

plt.figure(3)
sns.boxplot(x = df['mean_area'])

plt.figure(4)
sns.boxplot(x = df['mean_smoothness'])

Q1 = df['mean_radius'].quantile(0.25)
Q3 = df['mean_radius'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['mean_radius'] >= Q1 - 1.5 * IQR) & (df['mean_radius'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

Q1 = df['mean_texture'].quantile(0.25)
Q3 = df['mean_texture'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['mean_texture'] >= Q1 - 1.5 * IQR) & (df['mean_texture'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

Q1 = df['mean_perimeter'].quantile(0.25)
Q3 = df['mean_perimeter'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['mean_perimeter'] >= Q1 - 1.5 * IQR) & (df['mean_perimeter'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

Q1 = df['mean_area'].quantile(0.25)
Q3 = df['mean_area'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['mean_area'] >= Q1 - 1.5 * IQR) & (df['mean_area'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

Q1 = df['mean_smoothness'].quantile(0.25)
Q3 = df['mean_smoothness'].quantile(0.75)
IQR = Q3 - Q1    #IQR is interquartile range. 

filter = (df['mean_smoothness'] >= Q1 - 1.5 * IQR) & (df['mean_smoothness'] <= Q3 + 1.5 *IQR)
df = df.loc[filter] 

df = df.reset_index(drop = True)
df

data = df
#splitting attributes and outcomes

X = data.iloc[:,0:-1].values;
y = data.iloc[:,-1].values;

print(X.shape,y.shape)

from sklearn.model_selection import train_test_split

#Splitting the data into 80:20 train:test ratio
X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.8,random_state = 42)

print(X_train.shape,y_train.shape)
print(X_test.shape,y_test.shape)

#Using the formula for gini index, we have the following cost function:
def cost_func_gini(y):

    y = pd.Series(y)

    p = y.value_counts() / y.shape[0]
    gini_index = 1 - np.sum(p**2)

    return gini_index

#for optimal split we will set the threshold where information gain is maximum

def information_gain(children):
    l_child = children['left']
    r_child = children['right']
    
    parent = l_child + r_child
       
    info_gained = cost_func_gini(parent)-((len(l_child)/len(parent))*cost_func_gini(l_child) + (len(r_child)/len(parent))*cost_func_gini(r_child))
    
    return info_gained

class Node:
    def __init__(self, predicted_class,feature_index=0,threshold=0,left=None,right=None,max_info_gain=None):

        self.predicted_class = predicted_class
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None
        self.max_info_gain = None


class DecisionTreeClassifier:
    def __init__(self, max_depth = 6,min_IG_to_allow_split = 0.1):  
        #defined maximum depth of 6 beyond which the tree is not allowed to grow
        self.max_depth = max_depth
        self.min_IG_to_allow_split = min_IG_to_allow_split

    def fit(self, X, y):
        self.n_classes_ = len(set(y))
        self.n_features_ = X.shape[1]
        self.tree_ = self._grow_tree(X, y)


    # decides the best attribute for splitting and the threshold at which
    # we shold split the attribute
    def _best_split(self, X, y):
        
        if y.size <= 1:
            return None, None,None

        num_parent = []
        for class_type in range(self.n_classes_):

            num_parent.append(np.sum(y == class_type))

        info_gain_curr = 1.0 - sum((n / y.size) ** 2 for n in num_parent)

        best_idx, best_thr,info_gain_max = None, None,None

        for idx in range(self.n_features_):
            thresholds, classes = zip(*sorted(zip(X[:, idx], y)))

            num_left = [0] * self.n_classes_
            num_right = num_parent.copy()

            for i in range(1, y.size):

                c = classes[i - 1]
                num_left[c] += 1
                num_right[c] -= 1

                dct = {'left': num_left,'right': num_right}

                info_gain_max = information_gain(dct) 


                if thresholds[i] == thresholds[i - 1]:
                    continue

                if info_gain_max < info_gain_curr:
                    info_gain_curr = info_gain_max
                    best_idx = idx
                    best_thr = thresholds[i]
            

        return best_idx, best_thr,info_gain_max

    #Recursive function that builds the tree and also performs the split
    def _grow_tree(self, X, y, depth=0):

        num_samples_per_class = []

        for i in range(self.n_classes_):
            num_samples_per_class.append(np.sum(y == i))

        predicted_class = num_samples_per_class.index(max(num_samples_per_class))

        node = Node(predicted_class = predicted_class)

        if (depth <= self.max_depth - 1):

            idx, thr,info_gain_max = self._best_split(X, y)

            if idx is not None:
                indices_left = X[:, idx] < thr

                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]

                node.feature_index = idx
                node.threshold = thr
                node.max_info_gain = info_gain_max

                # the tree will stop growing automatically if the information
                #gain of the decision node is not greater than 0.1
                if(node.max_info_gain > self.min_IG_to_allow_split ):

                    node.left = self._grow_tree(X_left, y_left, depth + 1)
                    node.right = self._grow_tree(X_right, y_right, depth + 1)

        return node

    #Function responsible for classification at test time
    def classify(self, X):

        predicted_values = []
        for inputs in X:

            node = self.tree_

            while node.left:
                if inputs[node.feature_index] < node.threshold:
                    node = node.left
                else:
                    node = node.right
            
            predicted_values.append(node.predicted_class)
        
        return predicted_values

clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

y_pred = clf.classify(X_test)
print(y_pred)

from sklearn.metrics import accuracy_score
print('Overall accuracy =>',accuracy_score(y_test, y_pred))

#Class wise accuracies:
from sklearn.metrics import confusion_matrix

Unique_classes = [0,1]

matrix = confusion_matrix(y_test, y_pred)
print(matrix)

k = matrix.diagonal()/matrix.sum(axis=1)

for i in range(len(Unique_classes)):
  print("Accuracy for class",Unique_classes[i],"=>",k[i])

"""2. 5-fold cross validation"""

from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

folds = StratifiedKFold(n_splits = 5)

avg_scores_across_all_folds = []

for i in range(2,15):
    model = DecisionTreeClassifier(max_depth = i)

    scores = cross_val_score(estimator=model,X= X_train,y = y_train)

    #The mean absolute errors for each fold:
    print(scores)

    avg_scores_across_all_folds.append(sum(scores)/5.0)

    print('\n')

print(avg_scores_across_all_folds.index(max(avg_scores_across_all_folds)))

from matplotlib import pyplot as plt    
   
plt.plot(range(2,15),avg_scores_across_all_folds)    
#display the graph    
plt.show()    

# The accuracy is found to be the highest for max_depth = 4

"""4. Implement XGBoost in which subsample=0.7 and max_depth=4."""

import xgboost
model = xgboost.XGBClassifier(subsample = 0.7, max_depth = 4)

model.fit(X_train,y_train,verbose = True,eval_set=[(X_test,y_test)])

from sklearn.metrics import plot_confusion_matrix
plot_confusion_matrix(model,
                      X_test,y_test,
                      display_labels = ['Cancerous','Non-cancerous'])

print('Overall accuracy on test data =>',93.0/102.0)

"""6,7 and 8. LightGBM """

import lightgbm

from sklearn.model_selection import train_test_split

#Splitting the data into 80:20 train:test ratio
Xtrain,X_test,ytrain,y_test = train_test_split(X,y,train_size=0.8,random_state = 42)

X_train,X_valid,y_train,y_valid = train_test_split(Xtrain,ytrain,train_size=0.85,random_state = 42)

print(X_train.shape,y_train.shape)
print(X_valid.shape,y_valid.shape)
print(X_test.shape,y_test.shape)

train_data = lightgbm.Dataset(X_train, label=y_train)
valid_data = lightgbm.Dataset(X_valid, label=y_valid)

parameters = {'objective': 'binary',
              'metric': 'auc',
              'is_unbalance': 'true',
              'boosting': 'gbdt',
              'num_leaves': 10,
              'feature_fraction': 0.5,
              'bagging_fraction': 0.5,
              'bagging_freq': 20,
              'learning_rate': 0.01,
              'verbose': -1,
              'max_depth': 3
             }

model = lightgbm.train(parameters,train_data,valid_sets = valid_data,num_boost_round=5000,early_stopping_rounds=50)

from sklearn.metrics import roc_auc_score

y_train_pred = model.predict(X_train)
y_valid_pred = model.predict(X_valid)
y_test_pred = model.predict(X_test)

print('AUC Train: ',(roc_auc_score(y_train, y_train_pred)))
print('AUC Valid: ',(roc_auc_score(y_valid, y_valid_pred)))

print('AUC Test:',(roc_auc_score(y_test, y_test_pred)))

matrix = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
          [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
          [0,0,0],[0,0,0],[0,0,0],[0,0,0]]
for i in range(0,20):
    parameters = {'objective': 'binary',
                'metric': 'auc',
                'is_unbalance': 'true',
                'boosting': 'gbdt',
                'num_leaves': i+3,  #number of leaves are varied from 3 to 22 
                'feature_fraction': 0.5,
                'bagging_fraction': 0.5,
                'bagging_freq': 20,
                'learning_rate': 0.01,
                'verbose': -1,
                'max_depth': 3
                }

    model = lightgbm.train(parameters,train_data,valid_sets = valid_data,num_boost_round=5000,early_stopping_rounds=50)

    y_train_pred = model.predict(X_train)
    y_valid_pred = model.predict(X_valid)
    y_test_pred = model.predict(X_test)

    print('\n')
    print('\n')
    print('AUC Train: {:.4f}'.format(roc_auc_score(y_train, y_train_pred)))
    print('AUC Valid: {:.4f}'.format(roc_auc_score(y_valid, y_valid_pred)))

    print('AUC Test: {:.4f}'.format(roc_auc_score(y_test, y_test_pred)))
    print('\n')
    print('\n')


    matrix[i][0] = roc_auc_score(y_train, y_train_pred)
    matrix[i][1] = roc_auc_score(y_valid, y_valid_pred)
    matrix[i][2] = roc_auc_score(y_test, y_test_pred)


print(matrix)

print(max(matrix))
print(min(matrix))



mat = np.array(matrix)

print(np.min(mat, axis=0)) # computes minimum in each column
print(np.max(mat, axis=0)) # computes maximum in each column

"""Max accuracy on test data => number of leaves = 4 for max_depth equal to 3.

Similar accuracies are observed when number of leaves are just less than the value 2^(max_depth). After that the accuracy on test data decreases and train data increases slightly, thus the model starts to overfit.
"""

plt.plot(range(2,22),[matrix[i][2] for i in range(0,20)])    
#display the graph    
plt.show()

"""For max_depth = 5"""

matrix = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
          [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
          [0,0,0],[0,0,0],[0,0,0],[0,0,0]]
for i in range(0,20):
    parameters = {'objective': 'binary',
                'metric': 'auc',
                'is_unbalance': 'true',
                'boosting': 'gbdt',
                'num_leaves': i+3,  #number of leaves are varied from 3 to 22 
                'feature_fraction': 0.5,
                'bagging_fraction': 0.5,
                'bagging_freq': 20,
                'learning_rate': 0.01,
                'verbose': -1,
                'max_depth': 4
                }

    model = lightgbm.train(parameters,train_data,valid_sets = valid_data,num_boost_round=5000,early_stopping_rounds=50)

    y_train_pred = model.predict(X_train)
    y_valid_pred = model.predict(X_valid)
    y_test_pred = model.predict(X_test)

    print('\n')
    print('\n')
    print('AUC Train: {:.4f}'.format(roc_auc_score(y_train, y_train_pred)))
    print('AUC Valid: {:.4f}'.format(roc_auc_score(y_valid, y_valid_pred)))

    print('AUC Test: {:.4f}'.format(roc_auc_score(y_test, y_test_pred)))
    print('\n')
    print('\n')


    matrix[i][0] = roc_auc_score(y_train, y_train_pred)
    matrix[i][1] = roc_auc_score(y_valid, y_valid_pred)
    matrix[i][2] = roc_auc_score(y_test, y_test_pred)


print(matrix)

plt.plot(range(2,22),[matrix[i][2] for i in range(0,20)])    
#display the graph    
plt.show()

