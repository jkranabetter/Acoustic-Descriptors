import csv
from nltk.stem import *
from nltk.stem.porter import *
import gensim.downloader as api
from gensim.models import Word2Vec
import nltk
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 

"""
Plot at https://projector.tensorflow.org/ with
Perplexity: 5
Leaning rate: 10
Supervise: 10
"""

stemmer = PorterStemmer()
wv = api.load('word2vec-google-news-300') # Number of words not found in the word2vec model: 33  (total=  385 )

nltk.download('brown')
model = Word2Vec(brown.sents())

nltk.download('wordnet')
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

def get_embeddings_questions(descriptor_t, emotion_t, descriptor_questions, emotion_questions):

    missed_words = []
    emotion_words = []
    descriptor_words = []

    # get vectors for descriptors
    descriptor_vectors = []
    descriptor_qs = []
    for idx, x in enumerate(descriptor_t):
        try:
            # remove duplicates
            if x not in descriptor_words:
                descriptor_vectors.append(wv[x])
                descriptor_qs.append(descriptor_questions[idx])
                descriptor_words.append(x)
        except (KeyError, TypeError):
            missed_words.append(x)
            pass

    # get vectors for emotions
    emotion_vectors = []
    emotion_qs = []
    for idx, x in enumerate(emotion_t):
        try:
            # remove duplicates
            if x not in emotion_words:
                emotion_vectors.append(wv[x])
                emotion_qs.append(emotion_questions[idx])
                emotion_words.append(x)
        except (KeyError, TypeError):
            missed_words.append(x)
            pass

    print('Number of words not found in the word2vec model:', len(missed_words), ' (total= ', len(all_tags), ')')

    return descriptor_vectors, emotion_vectors, descriptor_words, emotion_words, descriptor_qs, emotion_qs


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


# get embeddins with corresponding question numbers
from extractors import extract_question_num
descriptor_tags, emotion_tags, descriptor_questions, emotion_questions = extract_question_num()
descriptor_vectors, emotion_vectors, descriptor_words, emotion_words, descriptor_qs, emotion_qs = get_embeddings_questions(descriptor_tags, emotion_tags, descriptor_questions, emotion_questions)

tensors_filename = 'outputfiles/tensors_questions.tsv'
tags_filename = 'outputfiles/tags_questions.tsv'

with open(tensors_filename, 'wt', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    for vector in descriptor_vectors:
        tsv_writer.writerow(vector)
    for vector in emotion_vectors:
        tsv_writer.writerow(vector)

with open(tags_filename, 'wt', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['word', 'Question'])
    for idx, descriptor in enumerate(descriptor_words):
        tsv_writer.writerow([descriptor_words[idx], descriptor_qs[idx]])
    for idx, emotion in enumerate(emotion_words):
        tsv_writer.writerow([emotion_words[idx], emotion_qs[idx]])