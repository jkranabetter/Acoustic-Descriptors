#Checking synonym for the word "travel"
from nltk.corpus import wordnet
import pandas as pd
from constants import *

# read from xlsx
df = pd.read_excel(LIBRARY_FILE, sheet_name='Sound Descriptors') 

# add items from the literature
for idx, row in df.iterrows():
    # collect all words
    row['Word'] = row['Word'].lower()

word_list = list(df['Word'])

print(len(word_list))
print(len(set(word_list)))

# write to xlsx
with pd.ExcelWriter(LIBRARY_FILE, mode='a', if_sheet_exists = 'replace') as writer:  
    df.to_excel(writer, sheet_name='Sound Descriptors', index = False)
