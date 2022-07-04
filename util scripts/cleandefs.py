import pandas as pd
from constants import *

"""
Script to bulk modify the definitions formatting in the descriptorslibrary.xlsx file.
"""

def main():

    # read from xlsx
    df = pd.read_excel(LIBRARY_FILE, sheet_name='Survey Descriptors') 

    for idx, row in df.iterrows():
        # find single definitions and remove the silly formatting
        meaning = str(row['Meaning'])
        if meaning.startswith("['"):
            if meaning.endswith("']"):
                if meaning.count(',') == 0:
                    clean_meaning = meaning[2:-2]
                    row['Meaning'] = clean_meaning

        # detect where I have missed inserting POS
        if row['Part of Speech'] == 'None':
            # print(row['Meaning'])
            if not pd.isna(row['Meaning']):
                print(row['Tag'])

        if not str(row['Meaning']).startswith('[') and str(row['Meaning']) != 'nan' and str(row['Meaning Number']) == 'nan':
            row['Meaning Number'] = 1

        # print(row['Tag'])

    # write to xlsx
    with pd.ExcelWriter(LIBRARY_FILE,
                        mode='a', if_sheet_exists = 'replace') as writer:  
        df.to_excel(writer, sheet_name='Survey Descriptors', index = False)

if __name__ == '__main__':
    main()