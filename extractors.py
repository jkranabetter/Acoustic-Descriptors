import csv
import re
import pandas as pd
from constants import *

# Extracts tags from the current processed tags file SURVEY_FILE
def extract_survey():
    descriptor_tags = []
    emotion_tags = []
    all_tags = []
    with open(SURVEY_FILE) as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        complete_counter = 0
        for row in csv_reader:
            # in current layour data is from row[17] to row[218]

            # skip column label rows
            if row[6] != "TRUE" and row[6] != "FALSE":
                continue
            
            # skip the response if not complete
            if row[6] == 'FALSE':
                continue

            # count complete responses
            if row[6] == 'TRUE':
                complete_counter += 1

            # go through row values
            for idx, item in enumerate(row):
                if(idx > 16 and idx < 219 and row[idx]):

                    # split string on a variety of symbols
                    # print(row[idx])
                    line_tags = re.split(pattern=r"[,./&]", string=row[idx])

                    # strip spaces from front end end of string
                    line_tags = [x.strip() for x in line_tags]

                    # convert to lower case
                    line_tags = [x.lower() for x in line_tags]

                    # remove empty strings
                    line_tags = [x for x in line_tags if x]

                    # split on or and and
                    for index, tag in enumerate(line_tags):
                        and_str = ' and '
                        or_str = ' or '
                        if and_str in tag:
                            split_tag = tag.split(and_str)
                            line_tags = line_tags[:index] + \
                                split_tag + line_tags[index+1:]
                        if or_str in tag:
                            split_tag = tag.split(or_str)
                            line_tags = line_tags[:index] + \
                                split_tag + line_tags[index+1:]

                    # store tags in appropriate lists
                    if idx % 2 == 0:
                        descriptor_tags = descriptor_tags + line_tags
                    else:
                        emotion_tags = emotion_tags + line_tags
                    all_tags = all_tags + line_tags

    # print('extracted results from %d complete resplonses'% complete_counter)
    # print('returning %d descripton and %d emotion tags'% (len(descriptor_tags), len(emotion_tags),))
    return all_tags, descriptor_tags, emotion_tags

# Extracts tags from the hand made descriptors sheet. 'SoundDescriptorsParsed'
def extract_literature():
 
    read_file = pd.read_excel (LIBRARY_FILE, sheet_name='SoundDescriptors')

    descriptors = list(read_file['Word'])

    # lower case
    descriptors = [x.lower() for x in descriptors]

    # remove duplicates
    descriptors = list(set(descriptors))

    print('returning %d tags from lit'% len(descriptors))
    return descriptors

def extract_question_num():
    read_file = pd.read_csv(SURVEY_FILE)

    descriptor_questions = []
    emotion_questions = []
    descriptor_tags = []
    emotion_tags = []
    for q_num in range(1,101):
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
                for x in range(1, clean_counter + 1):
                    emotion_questions.append(q_num)
            elif sub_q == 2:
                for t in clean_tags:
                    if t not in descriptor_tags:
                        clean_counter +=1
                        descriptor_tags.append(t)
                for x in range(1, clean_counter + 1):
                    descriptor_questions.append(q_num)
            else:
                print('error')

    return descriptor_tags, emotion_tags, descriptor_questions, emotion_questions