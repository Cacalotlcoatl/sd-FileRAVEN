# Resources:
# reST api Tutorial: https://restfulapi.net/
# REST HTTP Status Codes: https://restfulapi.net/http-status-codes/
# Civitai REST API https://github.com/civitai/civitai/wiki/REST-API-Reference

# TODO: start from scratch

import hashlib
import json
# import required modules
import os
from random import random

import nltk
from nltk.corpus import words

from ui import initialize_gui


def download_nltk_words():
    """
    Download the nltk words if they do not exist in the corpora/words directory.
    """
    if not os.path.exists(nltk.data.find('corpora/words')):
        nltk.download('words')


def generate_short_hash(hash_value):
    # Generates a short hash from the given hash value.
    # Args:
    #    hash_value (int): The hash value to generate a short hash from.
    # Returns:
    #    str: The short hash.
    # Truncate to 8 characters for a short hash
    short_hash = format(hash_value & 0xFFFFFFFF, 'x')[:8]
    return short_hash


def generate_hash(hashfile, hash_method):
    if hash_method == 'sha256':
        hash_obj = hashlib.sha256()
    elif hash_method == 'blurhash':
        hash_obj = hashlib.blake2b()
    else:
        raise ValueError('Invalid hash method')

    with open(hashfile, 'rb') as file:
        chunk = 0
        while chunk := file.read(8192):
            hash_obj.update(chunk)


# rename the model file and all supporting files according to the new name.
# Seek all files beginning with {old_name} and replace {old_name} with {
# new_name}
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


def lookup_model_info_local_file(model_name, model_path):
    """
    Lookup model info from a local file.

    Args:
        model_name (str): The name of the model.
        model_path (str): The path to the model.

    Returns:
        str: The model info.

    Raises:
        Exception: If the model info file is not found.
    """
    localfile_name = os.path.join(model_path, model_name + '.civitai.info')
    if os.path.exists(localfile_name):
        with open(localfile_name, 'r') as file:
            model_info = file.read()
        return model_info
    else:
        raise Exception('Model info File not found: ' + localfile_name)


# function lookup model information from local info file
def lookup_model_info_civitai(model_path, model_file, model_id, model_sh256):
    """
    Lookup model information from civitai using the provided model_URL,
    model_ID, and SHA256 hash.
    If the moIf the model_ID is known, the function skips the
    search. Otherwise,
    it queries the REST API endpoint with the SHA256 hash and retrieves the
    model_ID from the response. If no model ID is found, the function goes to
    the edit_model_info dialogue and skips the search. Finally, the function
    looks up the model information from civitai using the model_ID.
    """
    if not model_sh256:
        model_sh256 = generate_hash(model_file, 'sha256')
    if not model_id:
        endpoint_url = ('https://civitai.com/api/v1/model-versions/by-hash/' +
                        model_sh256)
        model_info = requests.get(endpoint_url)
        model_info_json = model_info.json()
        model_id = model_info_json['modelID']

        file_path = f"{model_path}/{model_name}.civitai.info"
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(model_info.text)

    if not model_id and model_sh256:
        model_id = lookup_model_id_civitai(model_sh256, '256')
    elif not model_id and model_blurhash:
        model_id = lookup_model_id_civitai(model_sh256, 'blur')
    if not model_id and model_sh256:
        model_id = lookup_model_id_civitai(model_sh256, '256')
    elif not model_id and model_blurhash:
        model_id = lookup_model_id_civitai(model_sh256, 'blur')

        # query REST API
    # endpoint with sha256
    # get model_id from response
    # If no model_id is found, go to edit_model_info dialogue and skip search
    # lookup model info from civitai using model_id

    if model_id:
        model_url = 'https://civitai.com/models/{model_id}/'
    return


def get_modelpage_title(model_id):
    """
    Get the title of the model page by making a GET request to the model's URL.

    Args:
        model_id (int): The ID of the model for which the title is to be
        retrieved.

    Returns:
        model_title (str): The title of the model page. If the GET request fails
        or the title is empty, returns None.
    """
    if not model_id:
        lookup_model_info_civitai(model_path, model_file, model_id, model_sh256)
        if not model_id:
            return None
    url = 'https://civitai.com/models/{model_id}/'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string
    soup = BeautifulSoup(response.text, 'html.parser')
    if title == '':
        return None
    else:
        print(title)
    return (title)


from bs4 import BeautifulSoup
import requests


# Make a request to the web page


# translate_to_1337 is to translate text from english to 1337. This is a
# simple version to start with.
def translate_to_1337(text):
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
    # Translates text from 1337 to English. It is beyond the scope of the
    # current project top support other languages. However, that
    # should not be too difficult to achieve by loading an alternate dictionary.

    # Args:
    #     leet_text (str): The text in 1337 to be translated.

    # Returns:
    #     str: The translated English text.

    nltk.download('words')
    english_words = set(words.words())
    english_text = ''.join(leet_map_reverse.get(c, c) for c in leet_text)
    # Check against the English dictionary
    decoded_words = []
    for word in english_text.split():
        if word.lower() in english_words:
            decoded_words.append(word)
        else:
            decoded_words.append(f'[{word}]')
    return ' '.join(decoded_words)

    # ----------------------------------------------------------------------
    # Initialize Main Program
    # Initialize global variables and dictionaries        
    #   leet_map is a dictionary for translating text from 1337 to English and
    #   back. The dictionary is loaded with a json file '1337.json'.


with open('1337_cipher.json', 'r') as file:
    leet_map = json.load(file)
    # Call the function to download the 'words' dataset if necessary
    download_nltk_words()
    # Initialize GUI
initialize_gui()

# MAIN LOOP
# call Main Menu
# select files to process
# determine naming pattern
# display proposed name and ask for permission to rename the model
# rename the model
