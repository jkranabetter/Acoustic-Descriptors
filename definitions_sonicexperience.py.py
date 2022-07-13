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

    # read from xlsx
    df = pd.read_excel(LIBRARY_FILE, sheet_name='Scrapes from Sonic Experience') 

    for idx, row in df.iterrows():
        print(f'Getting definition for {row["Word"]}')
        entry = get_meaning(row['Word'])
        df['Part of Speech'][idx] = entry['Part of Speech']
        df['Meaning'][idx] = entry['Meaning']
        if entry['Part of Speech'] != 'None':
            df['From'][idx] = 'WordNet'
        print(df)

    # write to xlsx
    with pd.ExcelWriter(LIBRARY_FILE,
                        mode='a', if_sheet_exists = 'replace') as writer:  
        df.to_excel(writer, sheet_name='Scrapes from Sonic Experience', index = False)

if __name__ == '__main__':
    main()