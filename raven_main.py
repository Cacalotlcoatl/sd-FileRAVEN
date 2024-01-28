# Resources:
# reST api Tutorial: https://restfulapi.net/
# REST HTTP Status Codes: https://restfulapi.net/http-status-codes/
# Civitai REST API https://github.com/civitai/civitai/wiki/REST-API-Reference

import hashlib
import json
# import required modules
import os

import nltk
from requests import Response

from raven_ui import initialize_gui


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
    If the model_ID is known, the function skips the search. Otherwise,
    it queries the REST API endpoint with the SHA256 hash and retrieves the
    model_info from the response. If no model is found, the function
    goes to the edit_model_info dialogue and skips the search. Finally,
    the function
    looks up the model page information from civitai using the model_ID.
    """
    if not model_sh256:
        model_sh256 = generate_hash(model_file, 'sha256')

    if not model_id:
        endpoint_url = ('https://civitai.com/api/v1/model-versions/by-hash/' +
                        model_sh256)
        model_info = requests.get(endpoint_url)
        model_info_json = model_info.json()
        model_id = model_info_json['modelId'].strip()
        file_path = f"{model_path}/{model_name}.civitai.info"
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(model_info.text)

    if model_id:
        model_url = 'https://civitai.com/models/{model_id}/'
        model_page: Response = requests.get(model_url)
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

# Initialize Main Program
def initialize_main_program():
    '''
    - Initialize global variables and dictionaries.
    '''
    # get current working directory
    cwd_path = os.getcwd()
    # set the path to the config file
    config_path = os.join(cwd_path, 'fileRAVEN.config')
    # Load the config file
    try:
        with open('fileRAVEN.config', 'r') as file:
            config = file.read()
            config = json.loads(config)
    except FileNotFoundError:
        # Handle the case where the file is not found
        print("The file 'fileRAVEN.config' was not found.")


'''
    - leet_map is a dictionary for translating text from 1337 to English and
    back. The dictionary is loaded with a json file '1337.json'. 
'''
try:
    with open('1337_cipher.json', 'r') as file:
        leet_map = json.load(file)
        # Call the function to download the 'words' dataset if necessary
        download_nltk_words()

# Initialize GUI
initialize_gui()

return
# ----------------------------------------------------------------------

initialize_main_program()

# MAIN LOOP
# call Main Menu
# select files to process
# determine naming pattern
# display proposed name and ask for permission to rename the model
# rename the model
