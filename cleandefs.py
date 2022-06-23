import pandas as pd
from constants import *

"""
Gets tags from descriptors_date.csv, gets definitions and writes to SoundDescriptorsParsed.
"""


def main():

    # read from xlsx
    df = pd.read_excel(LIBRARY_FILE, sheet_name='Survey Descriptors') 

    for idx, row in df.iterrows():
        meaning = str(row['Meaning'])
        if meaning.startswith("['"):
            if meaning.endswith("']"):
                if meaning.count(',') == 0:
                    clean_meaning = meaning[2:-2]
                    row['Meaning'] = clean_meaning

    # # write to xlsx
    # with pd.ExcelWriter(LIBRARY_FILE,
    #                     mode='a', if_sheet_exists = 'replace') as writer:  
    #     df.to_excel(writer, sheet_name='Survey Descriptors', index = False)

    # print(f'Done, added {new_desc_count} descriptors and {new_emo_count} emotions to the spreadsheet.')


if __name__ == '__main__':
    main()