import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
from numpy import genfromtxt
  
def plot_rooms():
    
    thedata_NY=np.genfromtxt(sys.argv[1],delimiter=',',dtype='str')
    thedata_SF=np.genfromtxt(sys.argv[2],delimiter=',',dtype='str')
    thedata_LA=np.genfromtxt(sys.argv[3],delimiter=',',dtype='str')

    p_NY=[]
    for row in thedata_NY:
        p_NY.append(eval(row))
    price_NY=[int(x) for x in p_NY]
    print(price_NY)

    
    p_SF=[]
    for row in thedata_SF:
        p_SF.append(eval(row))
    price_SF=[int(x) for x in p_SF]
    print(price_SF)

    p_LA=[]
    for row in thedata_LA:
        p_LA.append(eval(row))
    price_LA=[int(x) for x in p_LA]
    print(price_LA)

    plt.figure(figsize=(15,15))
    plt.subplot(311)
    plt.plot((price_NY),marker='o',linestyle='-.')
    plt.text(3,450,"New York")
    plt.ylim(0,500)
    plt.subplot(312)
    plt.plot((price_SF),marker='o',linestyle='-.')
    plt.text(3,450,"San Francisco")
    plt.ylim(0,500)
    plt.ylabel('nightly price [dollars]')
    plt.subplot(313)
    plt.plot((price_LA),marker='o',linestyle='-.')
    plt.text(3,450,"Los Angeles")
    plt.ylim(0,500)
    plt.xlabel('Numbers of listing')
    plt.subplots_adjust(0,0,0.5,0.5,0,0)
    plt.savefig('Price.eps',bbox_inches='tight',pad_inches = 0) 
    
if __name__ == '__main__':
  plot_rooms()
