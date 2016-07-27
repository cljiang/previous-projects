import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import pandas as pd

from numpy import genfromtxt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from math import radians, cos, sin, asin, sqrt
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
 
def analyze_rooms():
     
    fac=1   
   
    data_NY=pd.read_csv(sys.argv[1])
    data_SF=pd.read_csv(sys.argv[2])
    data_LA=pd.read_csv(sys.argv[3])

    X_NY=data_NY.iloc[:,[0,1,3,4]]
    y_NY=data_NY.iloc[:,2]
    X_train_NY,X_test_NY,y_train_NY,y_test_NY=train_test_split(X_NY,y_NY,random_state=42)
    
    X_SF=data_SF.iloc[:,[0,1,3,4]]
    y_SF=data_SF.iloc[:,2]
    X_train_SF,X_test_SF,y_train_SF,y_test_SF=train_test_split(X_SF,y_SF,random_state=42)

    X_LA=data_LA.iloc[:,[0,1,3,4]]
    y_LA=data_LA.iloc[:,2]
    X_train_LA,X_test_LA,y_train_LA,y_test_LA=train_test_split(X_LA,y_LA,random_state=42)
    
    plt.figure(figsize=(15,15))
    plt.subplot(311)
    plt.plot(y_NY*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.text(3,0.75,"New York")
    plt.ylim(0, 0.8)
    plt.subplot(312)
    plt.plot(y_SF*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.text(3,0.75,"San Francisco")
    plt.ylim(0, 0.8)
    plt.ylabel('Normalized Nightly Price')
    plt.subplot(313)
    plt.plot(y_LA*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.text(3,0.75,"Los Angeles")
    plt.ylim(0, 0.8)
    plt.xlabel('Numbers of listing')
    #plt.subplots_adjust(0,0,0.5,0.5,0,0)
    plt.savefig('PRICE.eps',bbox_inches='tight',pad_inches = 0) 

    #.boxplot.
    cities=np.vstack((y_NY,y_SF,y_LA)).T
    print((cities))
    box_colours = ['SkyBlue', 'LightGreen', 'Plum']
    locations = [1, 2, 3]
    plt.figure()
    plot2 = plt.boxplot(cities, 
                    widths=0.15,
                    notch=True,             # adds median notch
                    positions=locations,    # boxes locations
                    patch_artist=True,
                    )
    print(plot2['boxes'])
    print(box_colours)
    for box, colour in zip(plot2['boxes'], box_colours):
        plt.setp(box, color='Plum', 
             linewidth=1.5, 
             facecolor=colour)
    plt.setp(plot2['whiskers'], color='DarkMagenta', linewidth=1.5)
    plt.setp(plot2['caps'], color='DarkMagenta', linewidth=1.5)
    plt.setp(plot2['fliers'], color='OrangeRed', marker='o', markersize=10)
    plt.setp(plot2['medians'], color='OrangeRed', linewidth=1.5)
    names = ['New York', 'San Francisco', 'Los Angeles']
    plt.xticks(locations,               # tick marks
           names,                   # labels
           rotation='vertical')     # rotate the labels
    plt.savefig('BOXPLOT.eps',bbox_inches='tight',pad_inches = 0)


    plt.figure(figsize=(15,15))
    plt.subplot(311)
    plt.hist(y_NY*fac,range=[0,0.8], facecolor='gray')
    plt.text(0.8,140,"New York")
    plt.subplot(312)
    plt.hist(y_SF*fac,range=[0,0.8], facecolor='gray')
    plt.text(0.8,140,"San Francisco")
    plt.ylabel('Histograms')
    plt.subplot(313)
    plt.hist(y_NY*fac,range=[0,0.8], facecolor='gray')
    plt.text(0.8,140,"Los Angeles")
    #plt.subplots_adjust(0,0,0.5,0.5,0,0)
    plt.savefig('HIST.eps',bbox_inches='tight',pad_inches = 0) 

    #.linear regression
    linreg=LinearRegression()
    linreg.fit(X_train_NY,y_train_NY)
    zip([0,1,3,4],linreg.coef_)
    y_pred_NY=linreg.predict(X_test_NY)
    print(fac*metrics.mean_absolute_error(y_test_NY,y_pred_NY))

    linreg=LinearRegression()
    linreg.fit(X_train_SF,y_train_SF)
    zip([0,1,3,4],linreg.coef_)
    y_pred_SF=linreg.predict(X_test_SF)
    print(fac*metrics.mean_absolute_error(y_test_SF,y_pred_SF))
    
    linreg=LinearRegression()
    linreg.fit(X_train_LA,y_train_LA)
    zip([0,1,4],linreg.coef_)
    y_pred_LA=linreg.predict(X_test_LA)
    print(fac*metrics.mean_absolute_error(y_test_LA,y_pred_LA))

    plt.figure(figsize=(15,15))
    plt.subplot(311)
    plt.plot(y_test_NY*fac,y_pred_NY*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.plot([0, 0.4], [0, 0.4],linestyle='-',color='k')
    plt.text(0.01,0.35,"New York")
    plt.xlim(0,0.4)
    plt.ylim(0,0.4)
    plt.subplot(312)
    plt.plot(y_test_SF*fac,y_pred_SF*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.plot([0, 0.4], [0, 0.4],linestyle='-',color='k')                    
    plt.text(0.01,0.35,"San Francisco")
    plt.xlim(0,0.4)
    plt.ylim(0,0.4)
    plt.ylabel('Linear Regression Predicted Listings')
    plt.subplot(313)
    plt.plot(y_test_LA*fac,y_pred_LA*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.plot([0, 0.4], [0, 0.4],linestyle='-',color='k')                    
    plt.text(0.01,0.35,"Los Angeles")
    plt.xlim(0,0.4)
    plt.ylim(0,0.4)
    plt.xlabel('Test Listings')
    #plt.subplots_adjust(0,0,0.5,0.5,0,0)
    plt.savefig('LR.eps',bbox_inches='tight',pad_inches = 0) 

    #.Decision tree
    #np.random.seed(100)
    #dt=DecisionTreeRegressor()
    #dt.fit(X_train_NY,y_train_NY)
    #y_pred_dt_NY=dt.predict(X_test_NY)
    #print(metrics.mean_absolute_error(y_test_NY,y_pred_dt_NY))

    #.random forest
    rf=RandomForestRegressor(random_state=42)
    rf.fit(X_train_NY,y_train_NY)
    y_pred_rf_NY=rf.predict(X_test_NY)
    print(fac*metrics.mean_absolute_error(y_test_NY,y_pred_rf_NY))   

    rf=RandomForestRegressor(random_state=42)
    rf.fit(X_train_SF,y_train_SF)
    y_pred_rf_SF=rf.predict(X_test_SF)
    print(fac*metrics.mean_absolute_error(y_test_SF,y_pred_rf_SF))   

    rf=RandomForestRegressor(random_state=42)
    rf.fit(X_train_LA,y_train_LA)
    y_pred_rf_LA=rf.predict(X_test_LA)
    print(fac*metrics.mean_absolute_error(y_test_LA,y_pred_rf_LA))   

    plt.figure(figsize=(15,15))
    plt.subplot(311)
    plt.plot(y_test_NY*fac,y_pred_rf_NY*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.plot([0, 0.4], [0, 0.4],linestyle='-',color='k')                    
    plt.text(0.01, 0.35,"New York")
    plt.xlim(0,0.4)
    plt.ylim(0,0.4)
    plt.subplot(312)
    plt.plot(y_test_SF*fac,y_pred_rf_SF*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.plot([0, 0.4], [0, 0.4],linestyle='-',color='k')                    
    plt.text(0.01,0.35,"San Francisco")
    plt.xlim(0,0.4)
    plt.ylim(0,0.4)
    plt.ylabel('Random Forest Predicted Listings')
    plt.subplot(313)
    plt.plot(y_test_LA*fac,y_pred_rf_LA*fac,marker='o',linestyle='-.')
    plt.hold(True)
    plt.plot([0, 0.4], [0, 0.4],linestyle='-',color='k')                    
    plt.text(0.01,0.35,"Los Angeles")
    plt.xlim(0,0.4)
    plt.ylim(0,0.4)
    plt.xlabel('Test Listings')
    plt.savefig('RF.eps',bbox_inches='tight',pad_inches = 0) 

 
if __name__ == '__main__':
  analyze_rooms()
