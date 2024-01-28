# rename the model file and all supporting files according to the new name.
# Seek all files beginning with {old_name} and replace {old_name} with {
# new_name}
import os
from random import random

import nltk
from nltk.corpus import words
from raven

-main
import leet_map


def rename_model(model_path, old_name, new_name):
    # Rename files in the model_path that start with old_name to start with
    # new_name instead.
    #
    # Args:
    #   model_path(str): The path to the directory containing the files to be
    #       renamed.
    #   old_name(str): The prefix of the files to be replaced.
    #   new_name(str): The new prefix to replace old_name.
    #
    for filename in os.listdir(model_path):
        if filename.startswith(old_name):
            new_filename = filename.replace(old_name, new_name, 1)
            os.rename(os.path.join(model_path, filename), os.path.join(
                model_path, new_filename))


# concatenate model name with kwargs
# The function concatenate_model_name takes a string name_pattern as the first
# argument, which contains variables and literals separated and sequenced
# according to a specific pattern. The variables are represented within curly
# braces in the name_pattern string.
#
# The **kwargs in the function signature allows the function to accept any
# number of keyword arguments. These keyword arguments will be used to replace
# the variables within the curly braces in the name_pattern string.
#
# Inside the function, the .format(**kwargs) method is called on the
# name_pattern string. This method replaces the curly brace placeholders
# with the values provided in the kwargs dictionary. For example, if the
# name_pattern is "Model_{name}_{version}" and kwargs is
# {'name': 'abc', 'version': 'v1'}, then the .format(**kwargs) call will
# replace {name} with 'abc' and {version} with 'v1', resulting in the
# concatenated model name "Model_abc_v1"
def concatenate_model_name(name_pattern, **kwargs):
    return name_pattern.format(**kwargs)


def translate_to_1337(text, leet_map=None):
    """
    Translates the input text to 1337 speak using a predefined leet_map.
    Takes a text string as input.
    Returns the translated 1337 text string.
    """
    leet_text = ''
    for char in text:
        if char.upper() in leet_map:
            if char.upper() in 'AEIOU':
                if random.random() < 0.1:  # 90% chance of replacement for
                    # vowels
                    leet_text += random.choice(leet_map[char.upper()])
                else:
                    leet_text += char
            else:
                if random.random() < 0.2:  # 25% chance of replacement for
                    # consonants
                    leet_text += random.choice(leet_map[char.upper()])
                else:
                    leet_text += char
        else:
            leet_text += char
    return leet_text


def translate_from_1337(leet_text):
    '''
    Translates text from 1337 to English. It is beyond the scope of the
    current project top support other languages. However, that
    should not be too difficult to achieve by loading an alternate dictionary.

    Args:
        leet_text (str): The text in 1337 to be translated.

    Returns:
        str: The translated English text.
    '''
    nltk.download('words')
    english_words = set(words.words())
    english_text = ''.join(leet_map.get(c, c) for c in leet_text)
    # Check against the English dictionary
    decoded_words = []
    for word in english_text.split():
        if word.lower() in english_words:
            decoded_words.append(word)
        else:
            decoded_words.append(f'[{word}]')
    return ' '.join(decoded_words)
