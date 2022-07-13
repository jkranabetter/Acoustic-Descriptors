#Checking synonym for the word "travel"
from nltk.corpus import wordnet
import pandas as pd
from constants import *
import pickle

# read from xlsx
df_lit = pd.read_excel(LIBRARY_FILE, sheet_name='Sound Descriptors') 
df_survey = pd.read_excel(LIBRARY_FILE, sheet_name='Survey Descriptors') 

data = []

# add items from the literature
for idx, row in df_lit.iterrows():
    # collect all words
    words_set = (item[0] for item in data)
    
    # if we havent seen the word yet, add it
    if row['Word'] not in words_set:
        # print(row['Word'])
        data.append([row['Word'], row['Type'], row['Meaning'], row['Meaning Number'], row['From'], 'Literature', '', '', ''])

# add items from the survey
for idx, row in df_survey.iterrows():
    # collect all words
    words_set = (item[0] for item in data)

    # if we havent seen the word yet, add it
    if row['Tag'] not in words_set:
        # print(row['Word'])
        data.append([row['Tag'], row['Part of Speech'], row['Meaning'], row['Meaning Number'], row['From'], 'Survey', '', '', ''])

collated_df = pd.DataFrame(data, columns=['Word', 'Part of Speech', 'Meaning', 'Meaning Number', 'Meaning Source', 'Word Source', 'Synonym Group','Synonyms', 'Antonyms'])

# unpickle clustering groups dictionary
infile = open('wordclusters', 'rb')
word_clusters = pickle.load(infile)
infile.close

for idx, row in collated_df.iterrows():
    current_word = collated_df["Word"][idx]
    print(f'row {idx}, word: {collated_df["Word"][idx]}')

    if current_word in word_clusters.keys():
        collated_df.loc[collated_df['Word'] == row['Word'], 'Synonym Group'] = word_clusters[current_word]

# write to xlsx
with pd.ExcelWriter(LIBRARY_FILE, mode='a', if_sheet_exists = 'replace') as writer:  
    collated_df.to_excel(writer, sheet_name='Collated Data')
