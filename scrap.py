#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:12:44 2020

@author: dario
"""

from twitterscraper import *
import pandas as pd

search = 'protestas'
list_of_tweets = query_tweets(search, 100, lang = 'es')
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
import glob
import json
import re
import pandas as pd
from textblob import TextBlob
import boto3

comprehend = boto3.client('comprehend', region_name='us-east-2',aws_access_key_id='',aws_secret_access_key='')

from stop_words import get_stop_words
stop_words = get_stop_words('es')

directory = 'twitts_twitterscrapper/*'
def load_from_dir(directory):
  data = []
  for i in glob.glob(directory):
    with open(i) as json_file:
        data_1 = json.load(json_file)
        data.extend(data_1)
  return data

def preprocessing(line):
    url_regex = re.compile('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    line = line.lower()
    line = re.sub(r"[#, {}, \n]", " ", line)
    words = line.split(' ')
    words = [i for i in words if i != '' and i not in stop_words and 'http' not in i and '@' not in i]    
    line = ' '.join([a for a in words if not url_regex.match(a) and a[0] != '@' and a[0] != '@'])+'.'
    return line
    
def analyze_sentiment(data):
  counter = 0
  for i in data:
    if'positive' not in i:
#      print(preprocessing(i['text']))
      if preprocessing(i['text']) != '' :
        i['processed'] = preprocessing(i['text'])
        aws_sentiment = comprehend.detect_sentiment(Text=i['processed'], LanguageCode='es')
        i['sentiment'] = aws_sentiment['Sentiment']
        i['mixed'] = aws_sentiment['SentimentScore']['Mixed']
        i['negative'] = aws_sentiment['SentimentScore']['Negative']
        i['neutral'] = aws_sentiment['SentimentScore']['Neutral']
        i['positive'] = aws_sentiment['SentimentScore']['Positive']
      else:
        i['drop'] = 'drop'
      print(counter)
      counter +=1
  data = [i for i in data if 'drop' not in i]
  return data
#%%
Data = analyze_sentiment(tweets)