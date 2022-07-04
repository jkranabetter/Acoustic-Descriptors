from lib2to3.pgen2.token import SLASH
from extractors import extract_survey
import pandas as pd
from PyDictionary import PyDictionary
from constants import *

"""
Gets tags from survey, gets definitions and writes to DescriptorsLibrary.
"""

dictionary=PyDictionary()

def get_meaning(w):
    meaning = dictionary.meaning(w)
    Tag = {'Tag': w}
    try:
        if 'Adjective' in meaning:
            print (w + ' - Adjective', '\n', meaning['Adjective'], '\n\n\n')
            Tag['Part of Speech'] = 'Adjective'
            Tag['Meaning'] = meaning['Adjective']
        elif 'Verb' in meaning:
            print (w + ' - Verb', '\n', meaning['Verb'], '\n\n\n')
            Tag['Part of Speech'] = 'Verb'
            Tag['Meaning'] = meaning['Verb']
        elif 'Noun' in meaning:
            print (w + ' - Noun', '\n', meaning['Noun'], '\n\n\n')
            Tag['Part of Speech'] = 'Noun'
            Tag['Meaning'] = meaning['Noun']
        Tag['From'] = 'WordNet'
    except(TypeError):
        print(w+' - No REF \n\n\n')
        Tag['Part of Speech'] = 'None'
        Tag['Meaning'] = ''
    return Tag

def main():

    # get clean survey tags
    all_tags, descriptor_tags, emotion_tags = extract_survey()
    descriptor_tags = list(set(descriptor_tags))
    emotion_tags = list(set(emotion_tags))

    # check for multiple word tags (tags with a space)
    for item in (descriptor_tags + emotion_tags):
        items = item.split(' ')
        if len(items) > 1:
            print('WARNING ADDRESS FORMATTING: %s'% item)
    print()

    # # create dataframe
    # column_names = ['Tag', 'Class', 'Part of Speech', 'Meaning', 'Meaning Number', 'From']
    # df = pd.DataFrame(columns = column_names)

    # read from xlsx
    df = pd.read_excel(LIBRARY_FILE, sheet_name='Survey Descriptors') 

    df_descriptors = df.loc[df['Class'] == 'Descriptor']
    df_emotions = df.loc[df['Class'] == 'Emotion']

    # check if Tag/Class pair already in df
    new_desc_count = 0
    for tag in descriptor_tags:
        tag_exists = False
        for index, row in df_descriptors.iterrows():
            if (row['Tag'] == tag):
                tag_exists = True
                break
        # if not get definition and add to df
        if tag_exists == False:
            print(f'cant find {tag}, getting meaning and adding...')
            entry = get_meaning(tag)
            entry['Class'] = 'Descriptor'
            df = df.append(entry, ignore_index=True)
            new_desc_count +=1

    # check if Tag/Class pair already in df
    new_emo_count = 0
    for tag in emotion_tags:
        tag_exists = False
        for index, row in df_emotions.iterrows():
            if (row['Tag'] == tag):
                tag_exists = True
                break
        # if not get definition and add to df
        if tag_exists == False:
            print(f'cant find {tag}, getting meaning and adding...')
            entry = get_meaning(tag)
            entry['Class'] = 'Emotion'
            df = df.append(entry, ignore_index=True)
            new_emo_count += 1

    # write to xlsx
    with pd.ExcelWriter(LIBRARY_FILE,
                        mode='a', if_sheet_exists = 'replace') as writer:  
        df.to_excel(writer, sheet_name='Survey Descriptors', index = False)

    print(f'Done, added {new_desc_count} descriptors and {new_emo_count} emotions to the spreadsheet.')


if __name__ == '__main__':
    main()