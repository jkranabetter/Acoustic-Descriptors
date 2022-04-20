import csv
from nltk.stem import *
from nltk.stem.porter import *
stemmer = PorterStemmer()

import gensim.downloader as api
wv = api.load('word2vec-google-news-300') # Number of words not found in the word2vec model: 33  (total=  385 )

from gensim.models import Word2Vec
import nltk
nltk.download('brown')
from nltk.corpus import brown
model = Word2Vec(brown.sents())

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()


def get_embeddings(descriptor_t, emotion_t):

    missed_words = []

    # get vectors for descriptors
    descriptor_vectors = []
    descriptor_words = []
    for x in descriptor_t:
        try:
            # remove duplicates
            if x not in descriptor_words:
                descriptor_vectors.append(wv[x])
                descriptor_words.append(x)
        except (KeyError, TypeError):
            missed_words.append(x)
            pass

    # get vectors for emotions
    emotion_vectors = []
    emotion_words = []
    for x in emotion_t:
        try:
            # remove duplicates
            if x not in emotion_words:
                emotion_vectors.append(wv[x])
                emotion_words.append(x)
        except (KeyError, TypeError):
            missed_words.append(x)
            pass

    print('Number of words not found in the word2vec model:', len(missed_words), ' (total= ', len(all_tags), ')')

    return descriptor_vectors, emotion_vectors, descriptor_words, emotion_words


def write_tensors(tensors_filename, tags_filename, descriptor_vectors, emotion_vectors, descriptor_words, emotion_words):
    
    with open(tensors_filename, 'wt', newline='') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        for vector in descriptor_vectors:
            tsv_writer.writerow(vector)
        for vector in emotion_vectors:
            tsv_writer.writerow(vector)

    with open(tags_filename, 'wt', newline='') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['word', 'type'])
        for descriptor in descriptor_words:
            tsv_writer.writerow([descriptor, 'descriptor'])
        for emotion in emotion_words:
            tsv_writer.writerow([emotion, 'emotion'])


# get word embeddings for survey words
from extractors import extract_survey
all_tags, descriptor_tags, emotion_tags = extract_survey()
all_tags = list(set(all_tags))
descriptor_tags = list(set(descriptor_tags))
emotion_tags = list(set(emotion_tags))

tensors_filename = 'outputfiles/tensors_survey.tsv'
tags_filename = 'outputfiles/tags_survey.tsv'

descriptor_vectors, emotion_vectors, descriptor_words, emotion_words = get_embeddings(descriptor_tags, emotion_tags)
print(len(descriptor_words))
print(len(emotion_words))
write_tensors(tensors_filename, tags_filename, descriptor_vectors, emotion_vectors, descriptor_words, emotion_words)


# get word embeddings for survey and literature words combined
from extractors import extract_literature
descriptors_csv = extract_literature()

# add descriptor lists and remove duplicates FIX THIS WHEN UPDATING LIT SHEET W EMOTION
descriptor_tags += descriptors_csv
descriptor_tags = list(set(descriptor_tags))
all_tags += descriptors_csv
all_tags = list(set(all_tags))

tensors_filename = 'outputfiles/tensors_all.tsv'
tags_filename = 'outputfiles/tags_all.tsv'

descriptor_vectors, emotion_vectors, descriptor_words, emotion_words = get_embeddings(descriptor_tags, emotion_tags)
print(len(descriptor_words))
print(len(emotion_words))
write_tensors(tensors_filename, tags_filename, descriptor_vectors, emotion_vectors, descriptor_words, emotion_words)
