#Checking synonym for the word "travel"
from nltk.corpus import wordnet
import pandas as pd
from constants import *

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
        data.append([row['Word'], row['Type'], row['Meaning'], row['Meaning Number'], row['From'], '', ''])

# add items from the survey
for idx, row in df_survey.iterrows():
    # collect all words
    words_set = (item[0] for item in data)

    # if we havent seen the word yet, add it
    if row['Tag'] not in words_set:
        # print(row['Word'])
        data.append([row['Tag'], row['Part of Speech'], row['Meaning'], row['Meaning Number'], row['From'], '', ''])

collated_df = pd.DataFrame(data, columns=['Word', 'Part of Speech', 'Meaning', 'Meaning Number', 'Source', 'Synonyms', 'Antonyms'])

for idx, row in collated_df.iterrows():
    synonyms = []
    antonyms = []

    # get synonyms
    for syn in wordnet.synsets(row['Word']):
        for lm in syn.lemmas():
            synonyms.append(lm.name())#adding into synonyms
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name()) #adding into antonyms 

    row['Synonyms'] = synonyms
    row['Antonyms'] = antonyms


# write to xlsx
with pd.ExcelWriter(LIBRARY_FILE, mode='a', if_sheet_exists = 'replace') as writer:  
    collated_df.to_excel(writer, sheet_name='Collated Data')
