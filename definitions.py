from lib2to3.pgen2.token import SLASH
from extractors import extract_survey
import pandas as pd
from PyDictionary import PyDictionary

"""
Gets tags from descriptors_date.csv, gets definitions and writes to SoundDescriptorsParsed.
Warning: Running this takes a few hours as writte.
Need to update to only get definitions where needed.
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

# get clean survey tags
all_tags, descriptor_tags, emotion_tags = extract_survey()
descriptor_tags = list(set(descriptor_tags))
emotion_tags = list(set(emotion_tags))

# check for multiple word tags
for item in (descriptor_tags + emotion_tags):
    items = item.split(' ')
    if len(items) > 1:
        print('WARNING ADDRESS FORMATTING: %s'% item)
print()

# create dataframe
column_names = ['Tag', 'Class', 'Part of Speech', 'Meaning', 'Meaning Number', 'From']
df = pd.DataFrame(columns = column_names)

# retrieve definitions where they exist
for tag in descriptor_tags:
    entry = get_meaning(tag)
    entry['Class'] = 'Descriptor'
    df = df.append(entry, ignore_index=True)

for tag in emotion_tags:
    entry = get_meaning(tag)
    entry['Class'] = 'Emotion'
    df = df.append(entry, ignore_index=True)

# write to xlsx
with pd.ExcelWriter('data\SoundDescriptorsParsed.xlsx',
                    mode='a', if_sheet_exists = 'replace') as writer:  
    df.to_excel(writer, sheet_name='Survey Descriptors', index = False)
