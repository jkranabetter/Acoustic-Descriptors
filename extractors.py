import csv
import re
import pandas as pd

SURVEY_FILE = 'data\descriptors_may18.csv'
LITERATURE_FILE = 'data\SoundDescriptors_Survey.csv'

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
 
    read_file = pd.read_excel ('data\SoundDescriptorsParsed.xlsx', sheet_name='SoundDescriptors')
    read_file.to_csv ('data\SoundDescriptors_Survey.csv', index = None, header=True)

    descriptors = []
    with open(LITERATURE_FILE) as data_file:
            csv_reader = csv.reader(data_file, delimiter=',')
            for row in csv_reader:
                if row[0]:
                    descriptors.append(row[0].strip().lower())

    # remove duplicates
    descriptors = list(set(descriptors))
    print('returning %d tags from lit'% len(descriptors))
    return descriptors

# extract_literature()
# extract_survey()