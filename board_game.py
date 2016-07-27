%matplotlib inline 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

board_games = pd.read_csv('board_games.csv')
print(board_games.head(5))
board_games.dropna(axis=0,how='any')
board_games = board_games[board_games['users_rated'] != 0]

plt.hist(board_games['average_rating'])
plt.show()
print(np.std(board_games['average_rating']))
print(np.mean(board_games['average_rating']))

kmeans_model = KMeans(n_clusters=5,random_state=1)
board_games = board_games.dropna(axis=0,how='any')
numeric_columns = board_games.drop(['name','type','id'],axis=1)
distances = kmeans_model.fit(numeric_columns)
labels = kmeans_model.labels_

game_mean = numeric_columns.apply(np.mean,axis=1)
game_std = numeric_columns.apply(np.std,axis=1)
plt.scatter(game_mean,game_std,c=labels)
plt.show()

correlations = numeric_columns.corr()
print(correlations['average_rating'])

predictors =['minage','total_wanters','average_weight']
reg = LinearRegression()
reg.fit(board_games[['average_weight']].values, board_games[['average_rating']].values)
predictions = reg.predict(board_games[['average_weight']].values)
rms = mean_squared_error(board_games['average_rating'],predictions)


