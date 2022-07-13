from constants import *
import pandas as pd
from nltk.cluster import KMeansClusterer
import nltk
from nltk.stem import *
from nltk.stem.porter import *
import gensim.downloader as api
from nltk.stem import WordNetLemmatizer 

"""
Cluster the word embeddings of all descriptor words and cluster them using k means clustering.
Returns a dictionary with words as keys and cluster numbers as values.
"""

NUM_CLUSTERS=40

def define_clusters():
    print('Loading word to vec model...')
    wv = api.load('word2vec-google-news-300') # Number of words not found in the word2vec model: 33  (total=  385 )

    # read from xlsx
    df_lit = pd.read_excel(LIBRARY_FILE, sheet_name='Sound Descriptors') 
    df_survey = pd.read_excel(LIBRARY_FILE, sheet_name='Survey Descriptors') 
    df_sonic = pd.read_excel(LIBRARY_FILE, sheet_name='Scrapes from Sonic Experience') 

    words = []
    # add items from the literature
    for idx, row in df_lit.iterrows():
        words_set = (item[0] for item in words)
        if row['Word'] not in words_set:
            words.append(row['Word'])
    # add items from the survey
    for idx, row in df_survey.iterrows():
        words_set = (item[0] for item in words)
        if row['Tag'] not in words_set:
            words.append(row['Tag'])
    # add items from the survey
    for idx, row in df_sonic.iterrows():
        words_set = (item[0] for item in words)
        if row['Word'] not in words_set:
            words.append(row['Word'])

    vectors = []
    valid_words = []
    for word in words:
        try:
            vectors.append(wv[word])
            valid_words.append(word)
        except:
            print(f'No embedding for {word}')
            continue

    kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25, avoid_empty_clusters=True)
    assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)

    word_clusters = {}
    for i, word in enumerate(valid_words):  
        word_clusters[word] = assigned_clusters[i]

    return word_clusters