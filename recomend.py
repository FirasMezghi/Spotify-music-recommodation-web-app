import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from process_data import *
import re


complete_feature_set_new=pd.read_csv('C:\\Users\\user\\spot_recom\\complete_feature.csv')
def process_song(df,complete_feature_set_new):
    complete_feature_song = create_feature_set(df)
    if len(complete_feature_song.columns)!=2165:
        complete_feature_song.insert(loc=2154, column='instrumentalness', value=df['instrumentalness'])
    complete_feature_song.to_csv("feature_son.csv",index=False)
    recomend=pd.DataFrame(complete_feature_set_new['id'])
    recomend['sim']=cosine_similarity(complete_feature_set_new.drop('id', axis = 1).values, complete_feature_song.drop('id', axis = 1).values)
    recomend_top_40 = recomend.sort_values('sim',ascending = False).head(40)
    return recomend_top_40
