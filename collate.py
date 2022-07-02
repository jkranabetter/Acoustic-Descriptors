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
        data.append([row['Word'], row['Type'], row['Meaning'], row['Meaning Number'], row['From'], '', '', ''])

# add items from the survey
for idx, row in df_survey.iterrows():
    # collect all words
    words_set = (item[0] for item in data)

    # if we havent seen the word yet, add it
    if row['Tag'] not in words_set:
        # print(row['Word'])
        data.append([row['Tag'], row['Part of Speech'], row['Meaning'], row['Meaning Number'], row['From'], '', '', ''])

collated_df = pd.DataFrame(data, columns=['Word', 'Part of Speech', 'Meaning', 'Meaning Number', 'Source', 'Synonym Group','Synonyms', 'Antonyms'])

syn_group = 0
group_index = 0
for idx, row in collated_df.iterrows():
    print(f'row {idx}, word: {collated_df["Word"][idx]}')
    group_found = False
    synonyms = []
    antonyms = []

    # get synonyms and antoyms
    for syn in wordnet.synsets(row['Word']):
        for lm in syn.lemmas():
            synonyms.append(lm.name())#adding into synonyms
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name()) #adding into antonyms 

    row['Synonyms'] = synonyms
    row['Antonyms'] = antonyms
    print(f'\t syns: {synonyms}')
    print(f'\t ants: {antonyms}')

    # check if any of the synonyms are in our word list
    if len(synonyms) > 0:
        fltr = collated_df['Word'].isin(synonyms)

        reduced_df = collated_df[fltr]
        print(reduced_df)

        # store all indeces of matches

        # if any of the matches have a group number, assign that number to all
        groups = list(reduced_df['Synonym Group'])
        groups = [item for item in groups if isinstance(item, int)]
        groups_set = set(groups)

        if len(groups_set) > 0:
            group_found = True
            min_group_num = min(groups_set)

        print(f'\t groups: {list(groups_set)}')

        if group_found:
            print('\t group found')
            # modify direct synonimous words to lowest idx
            collated_df.loc[collated_df['Word'] == row['Word'], 'Synonym Group'] = min_group_num
            collated_df.loc[collated_df['Word'].isin(synonyms), 'Synonym Group'] = min_group_num

            # for number in groups_set:
            #     # modify branch groups 
            #     collated_df.loc[collated_df.index.isin(groups_set), 'Synonym Group'] = min_group_num
                

        # if none have a group number, for all matches between synonyms and words in word list, assign a group number
        if not group_found:
            print('\t group NOT found')
            collated_df.loc[collated_df['Word'] == row['Word'], 'Synonym Group'] = group_index
            collated_df.loc[collated_df['Word'].isin(synonyms), 'Synonym Group'] = group_index
            group_index += 1
    # increment group number

    else:
        collated_df.loc[collated_df['Word'] == row['Word'], 'Synonym Group'] = group_index
        group_index += 1

    print()

# write to xlsx
with pd.ExcelWriter(LIBRARY_FILE, mode='a', if_sheet_exists = 'replace') as writer:  
    collated_df.to_excel(writer, sheet_name='Collated Data')
