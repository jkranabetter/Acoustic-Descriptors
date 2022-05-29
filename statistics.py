import extractors
import csv
import re

import pandas as pd
import numpy as np
from numpy import mean
from scipy.stats import trim_mean

import plotly.express as px
from collections import Counter
import enchant
dictionary = enchant.Dict("en_US")

QUALTRICS_FILE = 'data\qualtrics_raw.csv'
SURVEY_FILE = 'data\descriptors_may18.csv'
LITERATURE_FILE = 'data\SoundDescriptorsParsed.csv'

raw_stats = {}

def print_stats(title, library):
    print('-------------- %s --------------'%title)
    print('{:<35s}{:<8s}'.format('STAT', 'VALUE'))
    print('-----------------------------------------------')
    for key, value in library.items():
        if isinstance(value, (int, float)):
            print('{:<35s}{:<8.2f}'.format(key,float(value)))
    print()


dataframe = pd.read_csv(QUALTRICS_FILE)

# get participation stats
progress_df = dataframe['Progress']
progress_df = progress_df[2:]
progress = progress_df.values.tolist()
completion_count = progress.count('100')
total_responses = len(progress)
abandon_count = total_responses - completion_count

raw_stats['total responses'] = total_responses
raw_stats['completion count'] = completion_count
raw_stats['abandon count'] = abandon_count
raw_stats['completion rate %'] = (total_responses - abandon_count) / total_responses * 100

# get completion time stats
completes_df = dataframe[dataframe.Finished == 'True']
duration_df = completes_df['Duration (in seconds)']
duration = duration_df.tolist()
completion_times = list(map(int, duration))
completion_times = [seconds / 60 for seconds in completion_times]

raw_stats['average completion time (m)'] = mean(completion_times)
raw_stats['min completion time (m)'] = min(completion_times)
raw_stats['max completion time (m)'] = max(completion_times)
raw_stats['trim mean completion time (m)'] = trim_mean(completion_times, 0.2)

print_stats('SURVEY STATS', raw_stats)

# map the locations
latlong_df = completes_df[['LocationLatitude', 'LocationLongitude']]
fig = px.scatter_geo(completes_df,lat='LocationLatitude',lon='LocationLongitude').update_traces(marker=dict(color='red'))
fig.update_layout(title = 'World map', title_x=0.5)
fig.show()

# get clean survey tags
all_tags, descriptor_tags, emotion_tags = extractors.extract_survey()
descriptor_tags_set = set(descriptor_tags)
emotion_tags_set = set(emotion_tags)
all_tags_set = set(all_tags)

tags_in_both = descriptor_tags_set.intersection(emotion_tags_set)
tag_stats = {}
tag_stats['total tags'] = len(all_tags)
tag_stats['total unique tags'] = len(all_tags_set)
tag_stats['total unique tag/class pairs'] = len(emotion_tags_set) + len(descriptor_tags_set)
tag_stats['total descriptor tags'] = len(descriptor_tags)
tag_stats['unique descriptor tags'] = len(descriptor_tags_set)
tag_stats['total emotion tags'] = len(emotion_tags)
tag_stats['unique emotion tags'] = len(emotion_tags_set)
tag_stats['tags described as both'] = len(tags_in_both)
indict_count = 0
for t in all_tags_set:
    if dictionary.check(t):
        indict_count +=1
tag_stats['% tags in dictionary'] = indict_count/len(all_tags_set)*100




# read literature tags from xlsx
df = pd.read_excel('data\SoundDescriptorsParsed.xlsx', sheet_name='SoundDescriptors') 

lit_tag_stats = {}
lit_tag_stats['total tags'] = len(df)

# detect duplicates
lit_words = df['Word'].to_list()
lit_words = [w.lower() for w in lit_words]

for item in lit_words:
    if lit_words.count(item) > 1:
        print(f'WARNING: found duplicate in lit: {item}')

survey_coverage = 0
for t in lit_words:
    if t in all_tags_set:
        survey_coverage += 1
lit_tag_stats['% words in survey tags'] = survey_coverage/len(lit_words)*100
lit_tag_stats['% words not in survey tags'] = 100 - lit_tag_stats['% words in survey tags']

lit_coverage = 0
for t in all_tags_set:
    if t in lit_words:
        lit_coverage += 1
tag_stats['% words in lit words'] = lit_coverage/len(all_tags_set)*100
tag_stats['% not in lit words'] = 100 - tag_stats['% words in lit words']


# print the stats
print_stats('SURVEY TAG STATS', tag_stats)
print_stats('LITERATURE TAG STATS', lit_tag_stats)


print('-------TAGS IN BOTH EMOTION AND DESCRIPTOR---------------')
print(tags_in_both)
print()

print('-------MOST COMMON SURVEY TAGS------------')
occurence_count = Counter(all_tags).most_common(10)
print(occurence_count)
print()