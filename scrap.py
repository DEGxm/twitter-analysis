#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:12:44 2020

@author: dario
"""

from twitterscraper import *
import pandas as pd

search = 'coronavirus'
list_of_tweets = query_tweets(search, 100000)
#%%
tweets = []
for tweet in list_of_tweets:
    tweets.append(tweet.__dict__)
#    print(tweet.__dict__.keys())
#    for key in dir(tweet):
#        print('####')
#        print(key, type(getattr(tweet,key)))t
#        print('####')
#        print(getattr(tweet,key))
dataframe =  pd.DataFrame(tweets) 
dataframe.to_pickle(search+'.pkl') 

#%%
dataframe_from_pkl = pd.read_pickle(search+'.pkl')
#%%
from textblob import TextBlob

analysis = TextBlob("This is all wrong")
print(analysis.sentiment)

print(analysis.tags)

print(analysis.translate(to='es'))

print(dir(analysis))