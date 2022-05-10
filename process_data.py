import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import re
from sklearn.preprocessing import OneHotEncoder

playlistDF = pd.read_csv("C:\\Users\\user\\spot_recom\\music_featured_data.csv")
playlistDF.drop(columns=["Unnamed: 0",'Unnamed: 0.1'], inplace = True)

def drop_duplicates(df):
    '''
    Drop duplicate songs
    '''
    df['artists_song'] = df.apply(lambda row: row['artist_name']+row['track_name'],axis = 1)
    return df.drop_duplicates('artists_song')

songDF = drop_duplicates(playlistDF)
#print("Are all songs unique: ",len(pd.unique(songDF.artists_song))==len(songDF))




def select_cols(df):
       '''
       Select useful columns
       '''
       return df[['artist_name','id','track_name','danceability', 'energy', 'key', 'loudness', 'mode',
       'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', "artist_pop", "genres", "track_pop"]]



def playlist_preprocess(df):
    '''
    Preprocess imported playlist
    '''
    df = drop_duplicates(df)
    df = select_cols(df)
    #df = genre_preprocess(df)

    return df


def getSubjectivity(text):
  '''
  Getting the Subjectivity using TextBlob
  '''
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  '''
  Getting the Polarity using TextBlob
  '''
  return TextBlob(text).sentiment.polarity

def getAnalysis(score, task="polarity"):
  '''
  Categorizing the Polarity & Subjectivity score
  '''
  if task == "subjectivity":
    if score < 1/3:
      return "low"
    elif score > 1/3:
      return "high"
    else:
      return "medium"
  else:
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'
def sentiment_analysis(df, text_col):
  '''
  Perform sentiment analysis on text
  ---
  Input:
  df (pandas dataframe): Dataframe of interest
  text_col (str): column of interest
  '''
  df['subjectivity'] = df[text_col].apply(getSubjectivity).apply(lambda x: getAnalysis(x,"subjectivity"))
  df['polarity'] = df[text_col].apply(getPolarity).apply(getAnalysis)
  return df

sentiment = sentiment_analysis(songDF, "track_name")

enc = OneHotEncoder(handle_unknown='ignore')
X=sentiment[['subjectivity','polarity']]
enc.fit(X)

tfidf = TfidfVectorizer()
tfidf.fit(songDF['genres'])


pop = songDF[["artist_pop","track_pop"]].reset_index(drop = True)
scaler = MinMaxScaler()
scaler.fit(pop)









def create_feature_set(df):
    '''
    Process spotify df to create a final set of features that will be used to generate recommendations
    ---
    Input: 
    df (pandas dataframe): Spotify Dataframe
    float_cols (list(str)): List of float columns that will be scaled
            
    Output: 
    final (pandas dataframe): Final set of features 
    '''
    df=select_cols(df)
    # Tfidf genre lists
    tfidf_matrix =  tfidf.transform(df['genres'])
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
    #genre_df.drop(columns='genre|unknown') # drop unknown genre
    genre_df.reset_index(drop = True, inplace=True)
    
    # Sentiment analysis
    df = sentiment_analysis(df, "track_name")

    # One-hot Encoding
    X=df[['subjectivity','polarity']]
    enc_matrix = enc.transform(X)
    enc_df = pd.DataFrame(enc_matrix.toarray())
    enc_df.columns = [ i for i in enc.get_feature_names()]
    enc_df.reset_index(drop = True, inplace=True)

    pop = df[["artist_pop","track_pop"]].reset_index(drop = True)
    pop_scaled = pd.DataFrame(scaler.transform(pop), columns = pop.columns)

    float_cols = df.dtypes[df.dtypes == 'float64'].index.values
    floats = df[float_cols].reset_index(drop = True)
    new_scaler = MinMaxScaler()
    floats_scaled = pd.DataFrame(new_scaler.fit_transform(floats), columns = floats.columns)

    final = pd.concat([genre_df, floats_scaled, pop_scaled, enc_df], axis = 1)
    final['id']=df['id'].values

    return final
#complete_feature_set = create_feature_set(songDF)
#complete_feature_set.to_csv("C:\\Users\\user\\spot_recom\\complete_feature.csv", index = False)












