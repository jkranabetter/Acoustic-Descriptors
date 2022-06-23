from nlp import WordFilter
import os

descriptors = []

def get_descriptors(filename):

    print(f'extracting descriptors from: {filename}')
    
    with open(filename) as file:
        sicko_mode = False
        current_string = ''
        bracket_items = []
        while 1:
            # read by character
            char = file.read(1)         
            if not char:
                break
                
            if char == ']' or char == ')':
                sicko_mode = False
                bracket_items.append(current_string)
                current_string = ''

            if sicko_mode:
                current_string += char.lower()

            if char == '[' or char == '(':
                sicko_mode = True

        file.close()   

    all_words = []
    for item in bracket_items:
        items = item.split()
        all_words += items

    word_filter = WordFilter()

    output, discard, pos_tags = word_filter.pos_filter(all_words)

    output_set = list(set(output))

    return output_set


# assign directory
directory = 'movie_subs'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        movie_descriptors = get_descriptors(f)
        descriptors += movie_descriptors

descriptors = list(set(descriptors))
print(descriptors)

print(f'extracted {len(descriptors)} descriptors')
