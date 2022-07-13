import pandas as pd
from constants import *
from clustering import define_clusters

# read from xlsx
df_lit = pd.read_excel(LIBRARY_FILE, sheet_name='Sound Descriptors') 
df_survey = pd.read_excel(LIBRARY_FILE, sheet_name='Survey Descriptors') 
df_sonic = pd.read_excel(LIBRARY_FILE, sheet_name='Scrapes from Sonic Experience') 

data = []

def emotion_label(emo, non):
    emotion = ''
    if emo == 2:
        emotion = 'Emo'
    elif non == 1:
        emotion = 'Non-Emo'
    else:
        emotion = ''
    return emotion

# add items from the literature
for idx, row in df_lit.iterrows():
    # collect all words
    words_set = (item[0] for item in data)
    
    # if we havent seen the word yet, add it
    if row['Word'] not in words_set:
        emo = emotion_label(row['Emo'], row['Non-Emo'])
        data.append([row['Word'], row['Type'], row['Meaning'], row['Meaning Number'], row['From'], 'Literature', '', '', '', emo])

# add items from the survey
for idx, row in df_survey.iterrows():
    # collect all words
    words_set = (item[0] for item in data)

    # if we havent seen the word yet, add it
    if row['Tag'] not in words_set:
        emo = emotion_label(row['Emo'], row['Non-Emo'])
        data.append([row['Tag'], row['Part of Speech'], row['Meaning'], row['Meaning Number'], row['From'], 'Survey', '', '', '', emo])

# add items from Sonic Experience
for idx, row in df_sonic.iterrows():
    # collect all words
    words_set = (item[0] for item in data)

    # if we havent seen the word yet, add it
    if row['Word'] not in words_set:
        emo = emotion_label(row['Emo'], row['Non-Emo'])
        data.append([row['Word'], row['Part of Speech'], row['Meaning'], row['Meaning Number'], row['From'], 'Sonic Experience', '', '', '', emo])

collated_df = pd.DataFrame(data, columns=['Word', 'Part of Speech', 'Meaning', 'Meaning Number', 'Meaning Source', 'Word Source', 'Synonym Group','Synonyms', 'Antonyms', 'Emotion'])

# get clusters
word_clusters = define_clusters()

for idx, row in collated_df.iterrows():
    current_word = collated_df["Word"][idx]

    if current_word in word_clusters.keys():
        collated_df.loc[collated_df['Word'] == row['Word'], 'Synonym Group'] = word_clusters[current_word]

# write to xlsx
with pd.ExcelWriter(LIBRARY_FILE, mode='a', if_sheet_exists = 'replace') as writer:  
    collated_df.to_excel(writer, sheet_name='Collated Data')
