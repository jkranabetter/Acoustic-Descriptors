from constants import *
import pandas as pd

df_collate = pd.read_excel(LIBRARY_FILE, sheet_name='Collated Data') 

words = df_collate['Word']

print(len(words))
print(len(set(words)))