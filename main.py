
# Resources:
# reST api Tutorial: https://restfulapi.net/
# REST HTTP Status Codes: https://restfulapi.net/http-status-codes/
# Civitai REST API https://github.com/civitai/civitai/wiki/REST-API-Reference

# UTTER CHAOS!!! 
# TODO: start from scratch

import hashlib
# import required modules
import os

import requests  # for making http request
from bs4 import BeautifulSoup  # for scraping webpages

from ui import initialize_gui


# function generate sh256 or blurhash from target file
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


def generate_short_hash(hash_value):
    short_hash = format(hash_value & 0xFFFFFFFF, 'x')[
                 :8]  # Truncate to 8 characters for a short hash
    return short_hash


# rename the model file and all supporting files according to the new name.
# Seek all files beginning with {old_name} and replace {old_name} with {
# new_name}
def rename_model(model_path, old_name, new_name):
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


def lookup_model_info_localfile(model_name, model_path):
    # model info file {model_path)+{model_name}+".civitai.info"
    localfile_name = model_path + model_name + ".civitai.info"
    while localfile_name:
        if os.path.exists(localfile_name):
            with open(localfile_name, 'r') as file:
                model_info = file.read()
            return model_info
        else:
            error('File not found: ' + localfile_name)
        return


while
    return

# function lookup model information from local info file
def lookup_model_info_civitai(model_url, model_id, model_sh256):
    # if model_id is known, skip search, otherwise lookup model info from
    # civitai
    # query REST API endpoint with sha256
    # get model_id from response
    # If no model_id is found, go to edit_model_info dialogue and skip search
    # lookup model info from civitai using model_id
    return


def get_modelpage_title(model_id):
    url = 'https://civitai.com/models/{model_id}/'
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string

    print(title)
    return


# MAIN LOOP
# Initialize the gui
initialize_gui()

# call Main Menu
# select files to process
# determine naming pattern
# display proposed name and ask for permission to rename the model
# rename the model
