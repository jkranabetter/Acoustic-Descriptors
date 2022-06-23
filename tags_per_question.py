import pandas as pd
import csv
from constants import *

"""
generate the file that correlates question numbers, filenames, and the resulting emotion and descriptive tags
"""

read_file = pd.read_csv(SURVEY_FILE)

filenames = pd.read_csv(FILENAMES)

emo_lib = {}
desc_lib = {}

for q_num in range(1,101):
    emotion_tags = []
    descriptor_tags = []
    for sub_q in range(1,3):
        col_name = 'Q' + str(q_num) + '_' + str(sub_q)
        mylist = list(read_file[col_name])
        clean_tags = [item.split(',') for item in mylist[2:] if not(pd.isnull(item)) == True]
        clean_tags = [item for sublist in clean_tags for item in sublist]

        # convert to lower case
        clean_tags = [x.lower().strip() for x in clean_tags]

        # remove empty strings
        clean_tags = [x for x in clean_tags if x]

        clean_counter = 0
        if sub_q == 1:
            for t in clean_tags:
                if t not in emotion_tags:
                    clean_counter +=1
                    emotion_tags.append(t)

        elif sub_q == 2:
            for t in clean_tags:
                if t not in descriptor_tags:
                    clean_counter +=1
                    descriptor_tags.append(t)

    emo_lib[q_num] = emotion_tags
    desc_lib[q_num] = descriptor_tags

with open('data/tags_per_question.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Question Number', 'File Name', 'Emotion Tags', 'Descriptor Tags'])
    for x in range(1, 101):
        # find filename for a given quesion number
        filename = filenames.loc[filenames['Question'] == x, 'Filename'].values[0]
        writer.writerow([x, filename, emo_lib[x], desc_lib[x]])

