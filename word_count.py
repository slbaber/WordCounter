# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# Author: Sara Baber
# Date: 05/04/2020
# Course: CS261 Data Structures, Portfolio Project
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                w = w.lower()  # covert word to lowercase for case-insensitive comparisons
                if ht.contains_key(w):  # if word already exists as key in ht, add 1 to value to track count
                    value = ht.get(w)
                    ht.put(w, value+1)

                else:
                    ht.put(w, 1)  # if word does not exist in ht as key, add word as key and initialize value as 1
                    keys.add(w)  # add word to set of keys

    count_dict = {}  # initialize empty dictionary
    count_array = []  # initialize empty array

    for key in keys:  # for each key, get it's value from ht and then add key/value pair to count_dict
        value = ht.get(key)
        count_dict[key] = value

    for key in keys:  # for each key, add value/key pair to array for sorting
        count_array.append((count_dict[key], key))

    count_array = sorted(count_array, reverse=True)  # reverse sort count_array from largest to smallest value

    for i in range(len(count_array)):  # reswap key/value pairs to get (word, count) for each tuple in count_array
        count_array[i] = (count_array[i][1], count_array[i][0])

    return count_array[:number]  # return only the requested number of top words
