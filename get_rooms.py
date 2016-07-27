import urllib.request
import urllib.parse
import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import pandas as pd
import scipy.stats as stats
import math

URL = 'https://api.airbnb.com/v2/search_results?%s'

def get_rooms():
  params = urllib.parse.urlencode({
    'client_id': '3092nxybyb0otqw18e8nh5nty',
    'locale': 'en-US',
    'currency': 'USD',
    '_format': 'for_search_results',
    '_limit': '50',
    '_offset': sys.argv[1],
    'location': sys.argv[2],
    'min_bathrooms': '0',
    'min_bedrooms': '0',
    'min_beds': '0',
    'price_min': '40',
    'price_max': '3000',
    'min_num_pic_urls': '0',
    'sort': 1,
  }, quote_via=urllib.parse.quote)

  req = urllib.request.Request(URL % params, headers={'User-Agent': 'Mozilla/5.0'})
  with urllib.request.urlopen(req) as f:
    res = json.loads(f.read().decode('utf-8'))
    #print(json.dumps(res['search_results'], indent=4, sort_keys=True))
    
    idd=[]
    bathrooms=[]
    bedrooms=[]
    beds=[]
    price=[]
    rating=[]
    person_capacity=[]
    for listing in res['search_results']:
       idd.append(listing['listing']['id'])
       bathrooms.append(listing['listing']['bathrooms'])
       bedrooms.append(listing['listing']['bedrooms'])
       beds.append(listing['listing']['beds'])
       price.append(listing['pricing_quote']['nightly_price'])
       rating.append(listing['listing']['star_rating'])
       person_capacity.append(listing['listing']['person_capacity'])
 
    bathrooms=np.asarray(bathrooms,dtype=np.float)
    beds=np.asarray(beds,dtype=np.float)
    price=np.asarray(price,dtype=np.float)
    rating=np.asarray(rating,dtype=np.float)
    person_capacity=np.asarray(person_capacity,dtype=np.float)

    ind_zero=np.where(bathrooms==0)[0]
    bathrooms[ind_zero]=float('nan')  
    col_mean=stats.nanmean(bathrooms)
    ind_nan=np.where(np.isnan(bathrooms))
    bathrooms[ind_nan]=math.floor(col_mean)
    bathrooms=bathrooms/np.linalg.norm(bathrooms)
    print(bathrooms)   

    ind_zero=np.where(beds==0)[0]
    beds[ind_zero]=float('nan')
    ind_eight=np.where(beds>8)[0]
    beds[ind_eight]=float('nan')  
    col_mean=stats.nanmean(beds)
    ind_nan=np.where(np.isnan(beds))
    beds[ind_nan]=math.floor(col_mean)
    beds=beds/np.linalg.norm(beds)
    print(beds)   

    ind_zero=np.where(rating==0)[0]
    rating[ind_zero]=float('nan')  
    col_mean=stats.nanmean(rating)
    ind_nan=np.where(np.isnan(rating))
    rating[ind_nan]=math.floor(col_mean)
    rating=rating/np.linalg.norm(rating)
    print(rating)
   
    ind_zero=np.where(person_capacity==0)[0]
    person_capacity[ind_zero]=float('nan')  
    col_mean=stats.nanmean(person_capacity)
    ind_nan=np.where(np.isnan(person_capacity))
    person_capacity[ind_nan]=math.floor(col_mean)
    person_capacity=person_capacity/np.linalg.norm(person_capacity)
    print(person_capacity)

    ind_zero=np.where(price==0)[0]
    price[ind_zero]=float('nan')  
    col_mean=stats.nanmean(price)
    ind_nan=np.where(np.isnan(price))
    price[ind_nan]=math.floor(col_mean)
    print(np.linalg.norm(price))
    price=price/np.linalg.norm(price)
    print(price)
 
    #df=pd.DataFrame({'Nightly Price': price, 'Bathrooms': bathrooms, 'Beds': beds, 'Rating':rating,'Person Capacity': person_capacity})
  
    #with open(sys.argv[3], "ab") as MYfile:
       #np.savetxt(MYfile, df.values, fmt='%.4e',delimiter=',')
       ##df.to_csv(MYfile, header=True, index=True, sep=',', mode='a')

if __name__ == '__main__':
  get_rooms()
