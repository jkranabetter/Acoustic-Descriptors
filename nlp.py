# importing the nltk suite 
from turtle import pos
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import brown
from nltk.tag import UnigramTagger

'''
Basic NLP for AUME by Joshua Kranabetter Feb 2022.
NLTK part of speech (pos) tagging and word filtering based on tag type.

'''

class WordFilter(object):

    def __init__(self):

        # Using data
        train_sents = brown.tagged_sents()
        self.uni_tagger = UnigramTagger(train_sents)
        self.pos_discard_cache = []
        self.output_cache = []

        self.parts_of_speech_filter = {
            '$' : False,  # dollar   [, −, −, —, A, A, C, HK, HK, M, NZ, NZ, S, U.S., U.S, …
            '”' : False,  # closing quotation mark   [‘, ”]
            '(' : False,  # opening parenthesis      [(, [, {]
            ')' : False,  # closing parenthesis      [), ], }]
            ',' : False,  # comma    [,]
            '—' : False,  # dash     [–]
            '.' : False,  # sentence terminator      [., !, ?]
            ':' : False,  # colon or ellipsis        [:, ;, …]
            'CC' : False,  # conjunction, coordinating       [&, ‘n, and, both, but, either, et, for, less,…
            'CD' : False,  # numeral, cardinal       [mid-1890, nine-thirty, forty-two, one-tenth, …
            'DT' : False,  # determiner      [all, an, another, any, both, del, each, eithe…
            'EX' : False,  # existential there       [there]
            'FW' : False,  # foreign word    [gemeinschaft, hund, ich, jeux, habeas, Haemen…
            'IN' : False,  # preposition or conjunction, subordinating       [astride, among, uppon, whether, out, inside, …
            'JJ' : True,  # adjective or numeral, ordinal   [third, ill-mannered, pre-war, regrettable, oi…
            'JJR' : True,  # adjective, comparative         [bleaker, braver, breezier, briefer, brighter,…
            'JJS' : True,  # adjective, superlative         [calmest, cheapest, choicest, classiest, clean…
            'LS' : False,  # list item marker        [A, A., B, B., C, C., D, E, F, First, G, H, I,…
            'MD' : False,  # modal auxiliary         [can, cannot, could, couldn’t, dare, may, migh…
            'NN' : False,  # noun, common, singular or mass          [common-carrier, cabbage, knuckle-duster, Casi…
            'NNP' : False,  # noun, proper, singular         [Motown, Venneboerger, Czestochwa, Ranzer, Con…
            'NNPS' : False,  # noun, proper, plural          [Americans, Americas, Amharas, Amityvilles, Am…
            'NNS' : False,  # noun, common, plural   [undergraduates, scotches, bric-a-brac, produc…
            'PDT' : False,  # pre-determiner         [all, both, half, many, quite, such, sure, this]
            'POS' : False,  # genitive marker        [‘, ‘s]
            'PRP' : False,  # pronoun, personal      [hers, herself, him, himself, hisself, it, its…
            'PRP$' : False,  # pronoun, possessive   [her, his, mine, my, our, ours, their, thy, your]
            'RB' : True,  # adverb          [occasionally, unabatingly, maddeningly, adven…
            'RBR' : True,  # adverb, comparative    [further, gloomier, grander, graver, greater, …
            'RBS' : True,  # adverb, superlative    [best, biggest, bluntest, earliest, farthest, …
            'RP' : False,  # particle        [aboard, about, across, along, apart, around, …
            'SYM' : False,  # symbol         [%, &, ‘, ”, ”., ), )., *, +, ,., <, =, >, @…
            'TO' : False,  # “to” as preposition or infinitive marker        [to]
            'UH' : False,  # interjection    [Goodbye, Goody, Gosh, Wow, Jeepers, Jee-sus, …
            'VB' : False,  # verb, base form         [ask, assemble, assess, assign, assume, atone,…
            'VBD' : False,  # verb, past tense       [dipped, pleaded, swiped, regummed, soaked, ti…
            'VBG' : True,  # verb, present participle or gerund     [telegraphing, stirring, focusing, angering, j…
            'VBN' : False,  # verb, past participle          [multihulled, dilapidated, aerosolized, chaire…
            'VBP' : False,  # verb, present tense, not 3rd person singular   [predominate, wrap, resort, sue, twist, spill,…
            'VBZ' : False,  # verb, present tense, 3rd person singular       [bases, reconstructs, marks, mixes, displeases…
            'WDT' : False,  # WH-determiner          [that, what, whatever, which, whichever]
            'WP' : False,  # WH-pronoun      [that, what, whatever, whatsoever, which, who,…
            'WP$' : False,  # WH-pronoun, possessive         [whose]
            'WRB' : False,  # Wh-adverb      [how, however, whence, whenever, where, whereby…
            '“' : False,  # opening quotation mark   [`, “]
            'None': False,
        }

    def pos_filter(self, tokens):
        
        # if the input is a string, we tokenize the string, else its already a list
        if(isinstance(tokens, str)):
            print('ERROR: input to pos taggins is list of strings not a string')

        # get POS tags, a list of tuples
        pos_tags = pos_tag(tokens)

        # filter the tags, keeping only tags labelled true in the above parts filter
        output = [x[0] for x in pos_tags if self.parts_of_speech_filter[x[1]]]

        # add discards to a list
        discard = []
        discard += [x[0] for x in pos_tags if not self.parts_of_speech_filter[x[1]]]

        return output, discard, pos_tags

    def uni_filter(self, tokens):
        
        # if the input is a string, we tokenize the string, else its already a list
        if(isinstance(tokens, str)):
            print('ERROR: input to pos taggins is list of strings not a string')

        # get POS tags, a list of tuples
        pos_tags = self.uni_tagger.tag(tokens)

        pos_list = []
        for item in pos_tags:
            
            part = item[1]
            if len(part) > 3: print('yep: ', part)
            if part is None: part = 'None'
            pos_list.append([item[0], part])

        print('printing list')
        print(pos_list)

        # filter the tags, keeping only tags labelled true in the above parts filter
        output = [x[0] for x in pos_list if self.parts_of_speech_filter[str(x[1])]]

        # add discards to a list
        discard = []
        discard += [x[0] for x in pos_list if not self.parts_of_speech_filter[x[1]]]

        return output, discard, pos_list

    def tokenize(self, input):
        return word_tokenize(input)
