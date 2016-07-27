
import pandas as pd
import seaborn as sns

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from math import radians, cos, sin, asin, sqrt
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sknn.mlp import Regressor, Layer

data=pd.read_csv('train.csv')
data.head()
data.tail()
sns.pairplot(data,x_vars=['start_lng','start_lat', 'end_lng','end_lat', 'start_timestamp'], y_vars=['duration'])

def haversine(lon1,lat1,lon2,lat2):
    lon1,lat1,lon2,lat2=map(radians,[lon1,lat1,lon2,lat2])
    dlon=lon2-lon1
    dlat=lat2-lat1
    a=sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c=2*asin(sqrt(a))
    r=6371
    return c*r

start_lng=data.start_lng
start_lng_tuple= tuple(map(tuple, start_lng.values))
haversine(start_lng.values,start_lng.values,start_lng.values,start_lng.values)

feature_cols=['start_lng','start_lat','end_lng','end_lat','start_timestamp']
X=data[feature_cols]
y=data.duration
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=2)

#.linear regression %425
linreg=LinearRegression()
linreg.fit(X_train,y_train)
zip(feature_cols,linreg.coef_)
y_pred=linreg.predict(X_test)
print metrics.mean_absolute_error(y_test,y_pred)

#.Decision tree %322
np.random.seed(100)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

dt=DecisionTreeRegressor()
dt.fit(X_train,y_train)
y_pred_dt=dt.predict(X_test)
print metrics.mean_absolute_error(y_test,y_pred_dt)

#.random forest %247
rf=RandomForestRegressor(random_state=42)
rf.fit(X_train,y_train)
y_pred_rf=rf.predict(X_test)
print metrics.mean_absolute_error(y_test,y_pred_rf)

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25)
#.neural network %diverged
nn = Regressor(
    layers=[
        Layer("Rectifier", units=100),
        Layer("Softmax")],
    learning_rate=0.02,
    n_iter=10)

nn = Regressor(
    layers=[
          Layer("Rectifier", units=5),
          Layer("Linear")],
    learning_rate=0.0001,
    n_iter=20,
    momentum=0.5,
    algorithm="sgd")

nn.fit(X_train.as_matrix(), y_train.as_matrix()) 
y_pred_nn = nn.predict(X_test)
print metrics.mean_absolute_error(y_test,y_pred_nn)






