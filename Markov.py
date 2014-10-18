#!/usr/bin/env python

import sys, os
import random, twitter


def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""

    words = corpus.split()
    chains_dict = {}

    for i in range(len(words)-2):
        key = (words[i], words[i + 1])
        value = words[i+2]
        
        if key in chains_dict:
            chains_dict[key].append(value)
        else:
            chains_dict[key] = [value]

    return chains_dict

def make_text(chains_dictionary):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    

    random_key = random.choice(chains_dictionary.keys())

    while ord(random_key[0][0]) < 65 or ord(random_key[0][0]) > 90:
         random_key = random.choice(chains_dictionary.keys())
   
    seed_key = random_key
    

    output_string = seed_key[0] + ' ' + seed_key[1]
    
    while seed_key in chains_dictionary:
        options = chains_dictionary[seed_key]
        chosen_one = random.choice(options)
        output_string = output_string + ' ' + chosen_one
        sentence_enders = ['.', '!', '?']

        if len(output_string) < 139 and len(output_string) > 80 and output_string[-1] in sentence_enders:
            break
        else:
            if len(output_string) > 130:
                # last_word_removed = " ".join(output_string.split()[-1])
                output_string += random.choice(sentence_enders)
                break
            else:
                seed_key = (seed_key[1], chosen_one)

    if '"' in output_string:
        temp_output = (output_string.split('"'))
        output_string = "".join(temp_output)

    return output_string
    print output_string
    #print len(output_string)

def main():
    
    api = twitter.Api(consumer_key=os.environ.get('CONSUMER_KEY'), consumer_secret=os.environ.get('CONSUMER_SECRET'), access_token_key=os.environ.get('ACCESS_TOKEN'), access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'))

    args = sys.argv

    combined_text = ""

    for arg in args[1:]:
        raw_text = open(arg)
        text = raw_text.read().strip()
        combined_text = combined_text + ' ' + text



    chain_dict = make_chains(combined_text)

    api.PostUpdate(make_text(chain_dict))

if __name__ == "__main__":
    main()