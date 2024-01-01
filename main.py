"""
Project: sd-FileRAVEN (Reader-friendly Application for Validated Entity Naming)
    Developed by Brian Conroy

sd-FileRAVEN is a cross-platform utility designed to assist users in quickly
and effectively annotating and attributing models with information about base
model, author, and version. By retrieving information for models downloaded
from civitai.com and renaming the model files to user-friendly standardized
filenames, sd-FileRAVEN helps to eliminate duplicates, prevent confusion
between similarly or cryptically named models, enhances organization,
and streamlines the user's model library. With its ability to help eliminate
duplicates and to distinguish identically-named models, this application
proves to be an invaluable asset for model management.

Date of initial commit: December 15, 2023

PROJECT MAP
   project/
   ├── main.py         (Model renaming logic)
   ├── ui.py           (User Interface)
   ├── civitai.json    (CivitAI API info)
   └── templates/      (HTML templates for displaying model info)
       ├── base.html
       └── model.html

Default naming strategies:
  1. Limit filenames to a set of (mostly) universally acceptable characters:
      a. Lowercase letters
      b. Uppercase letters
      c. Numbers (0-9)
      d. Universally accepted Special characters (underscore, hyphen,
      period), parenthesis, brackets, braces
      e. Special characters: for parenthesis, brackets, and braces the user
      should be issued a permanently skippable warning with before file
        renaming operations:
            '''
			Heads up!
            Using parentheses (()), brackets ([]), or braces ({}) in
            filenames can lead to compatibility issues
            on some systems or with certain software.
            Here's why:
            FAT32 Restriction: These characters aren't allowed on FAT32 file
            systems, common on older Windows systems and portable drives.
            Software Quirks: Some older software or scripts might not handle
            them correctly, causing problems.
            Web Compatibility: Some web servers or applications might have
            restrictions on these characters in filenames.
            To ensure maximum compatibility, stick to letters, numbers,
            underscores (_), periods (.), and hyphens (-).
            If you must use these characters, proceed with caution and be
            aware of potential limitations.
			 '''
      f. Spaces: Issue a brief, permanently skippable warning:
            '''
			** Warning: While some systems allow spaces in filenames,
			they can lead to problems on others (older Windows,
			web servers, etc.).

			Consider using hyphens (-) instead for universal compatibility.**
			'''
  2. For filename elements (e.g. model_name, version_name, etc.), Strip the
  elements of any forbidden characters (use a class to define letters allowed
		and loop through the string adding only allowed characters) before
		adding them to the proposed new filename
  3. Model types: [(Checkpoint, TextualInversion, Hypernetwork,
  AestheticGradient, LORA, Controlnet, Poses]
  3. Model type default strategies for base_name:
      a. checkpoints and basemodels:
            default format: {title}_by_{creator_name}.{model_style}.{
            base_model}.{version_name}
         1. title:  the title from the model page. I have found that this is
         usually a much more descriptive and accurate name than the filename
         given.
         2. creator_name:  the name of the creator of the model.
         3. model_style:  the style of the model. Start with these categories
         and refine after testing and feedback:
            a. photo: photorealistic models
            b. multi: general purpose models. Models not tuned to specific
            output types, or tuned to multiple types, e.g. SD1.5 basemodel
            c. art: Non-photorealistic artistic styles
            d. trad: Traditional media styles (e.g., oilpaint, watercolor,
            sketch)
            e. cgi3d: Computer-generated 3D styles (e.g., Pixar, Unreal Engine)
            f. abst: Abstract imagery"line": linearts (e.g. anime, manga,
            sketch, charcoal, western traditional animation, comic book,
            cel-shaded, etc) style art
        b. Check model tags for keywords indicating the model represents a
        character, person, or celebrity, etc.
            1. If the model has a tag that matches any of these keywords,
            the model is a character. Check to see if it represents a real
            person
                a. check the "resembles_real_person" flag in the API
                response, if "true" exit the check loop.
                b. If the model tags include any of [influencer, celebrity,
                actor, actress, instagram, tiktok, pornstar, singer,
                adult model] set the "resembles_real_person flag to true and
                exit the check loop
                c. Look for "not a real person", "not real", "cartoon",
                "anime", "hentai", "game", "rpg", or "fictional character" in
                the title and text of the model page.
                d. If model tags include any of [fictional, ai character,
                anime, not real, cartoon, anime, hentai, game, rpg, etc.] set
                the "resembles_real_person flag to false and exit the check
                loop "
                e. if any of the above return positive:
                    1. break out of the check loop and set the
                    "resembles_real_person" flag to "false"
                    2. record the flag in the civitai.info file
                    3. else set the "resembles_real_person" flag to true and
                    record the value in the civitai.info file.
                    4. give the user the option to change the flag before
                    renaming the model.
                f. If "resembles_real_person" != "false" then real_tag = "true"
                    1. Note: I want to trap the possibility of an empty flag
                    and default to "true"

        LoRA and Hypernetworks:
        TextualInversion:

Resources:
reST api Tutorial: https://restfulapi.net/
REST HTTP Status Codes: https://restfulapi.net/http-status-codes/
Civitai REST API https://github.com/civitai/civitai/wiki/REST-API-Reference
"""
# UTTER CHAOS!!! 
# TODO: Sort new and old code snippets, index and standardize and stabilize variables, resequence for clarity

# import required modules
import hashlib
import json
import os
import re
from tkinter import filedialog

import requests
from PIL import Image


# ----------------------------------------------------------------
# Classes
# ----------------------------------------------------------------
class Grad_model:  # Aesthetic Gradients
    def __init__(self, file_path, file_name, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class CkPt_model:  # Fine-tuned Model Checkpoints includings checkpoints,
    # merges, and base-models
    def __init__(self, file_path, file_name, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class CNet_model:  # ControlNet models
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", ".ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt"),
            ("PyTorch Checkpoints Files", "*.pth")
        ]


class HN_model:  # Hypernetwork models
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class LS_model:  # Large-scale models (i.e. LoRA, LyCORIS, and LoHA models)
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class Other_model:  # Any model that does not fit the other model classes
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt"),
            ("any", "*.*")
        ]


class Seg_model:  # Segmentation models for aDetailer, SegmentAnything, etc.
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class TI_model:  # Textual Inversion models (a.k.a. embeddings)
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Binaries Files" "*.bin"),
            (" Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class Upscaler_model:  # VAE models
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class VAE_model:  # VAE models
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("Checkpoint Files", "*.ckpt"),
            ("Safety Tensors Files", "*.safetensors"),
            ("PyTorch Files", "*.pt")
        ]


class Image_files:
    def __init__(self)
        self.extensions = [
            ("Bit Mapped Image", "*.bmp"),
            ("Graphics Interchange Format Files", "*.gif"),
            ("Portable Network Graphic Files", "*.png"),
            ("Joint Photographic Experts Group Files", "*.jpg"),
            ("Joint Photographic Experts Group Files", "*.jpeg"),
            ("Joint Photographic Experts Group Files", "*.webp")
        ]


class Info_files:
    def __init__(self, file_path, title):
        self.file_path = file_path
        self.file_name = file_name
        self.title = title
        self.extensions = [
            ("JSON Files", "*.json"),
            ("Civitai Information Files", "*.civitai.info"),
            ("Comma Separated Values Files", "*.csv")
        ]

    def __init__(self, file_path):
        self.file_path = file_path

    def is_supported(self):
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower() in self.SUPPORTED_EXTENSIONS

    def load_image(self):
        if self.is_supported():
            try:
                image = Image.open(self.file_path)
                return image
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print(f"Unsupported file type: {self.file_path}")


# -----------------------------------------------------------------
# Constants
# -----------------------------------------------------------------
Gradio_Title = "FileRAVEN"
# Expand later to make the remote repository user settable,
# and allow for multiple remote repositories
rem_db_base_url = "https://api.civitai.com/v1/models"
rem_db_search_url = "https://api.civitai.com/v1/search"

# -----------------------------------------------------------------
# Functions
# -----------------------------------------------------------------

def is_supported(self):
    _, file_extension = os.path.splitext(self.file_name)
    return file_extension.lower() in self.SUPPORTED_EXTENSIONS



    
def get_sha256(file_path, chunk_size=8192):
    sha256_hash = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            sha256_hash.update(chunk)
        print(f"SHA-256 Hash for {file_path}: {sha256_hash}")
    return sha256_hash.hexdigest()


# Define a function to retrieve the model information from the Civitai API
def search_civitai(hash):
    # Construct the API request
    url = f"{civitai_api_url}?hash={hash}&limit=100"
    response = requests.get(url)
    
    # Parse the response
    data = response.json()
    
    # Extract the model information
    models = data["models"]
    
    # Return the model information
    return models


def get_model_info(model_name):
    # Construct the API request
    url = f"{civitai_api_url}{model_name}"
    response = requests.get(url)
    
    # Parse the JSON response
    data = json.loads(response.content)
    
    # Extract the relevant information
    model_info = {
        "model_name": data["name"],
        "creator_name": data["creator"]["name"],
        "version_name": data["version"]["name"],
        "base_model": data["base_model"]
    }
    
    return model_info
    
"""
Create a `Tk` window with a label, entry field, and button for renaming the model, a button for displaying the model information, and a button for exiting the program. The `rename_model` function will be called when the "Rename" button is clicked, and the `show_model_info` function will be called when the "Info" button is clicked.
"""

# Create a Tk instance and define a function to handle the user input
import tkinter as tk
from tkinter import messagebox

# Create the main window
window = tk.Tk()
window.title(Gradio_Title)

# Create a label and entry field for the model name
label = tk.Label(window, text="Model Name:")
label.pack()
entry_model_name = tk.Entry(window)
entry_model_name.pack()

# Create a label and button for renaming the model
label = tk.Label(window, text="Rename Model:")
label.pack()
button_rename = tk.Button(window, text="Rename", command=rename_model)
button_rename.pack()

# Create a label and button for displaying the model information
label = tk.Label(window, text="Model Information:")
label.pack()
button_info = tk.Button(window, text="Info", command=show_model_info)
button_info.pack()

# Create a label and button for exiting the program
label = tk.Label(window, text="")
label.pack()
button_exit = tk.Button(window, text="Exit", command=window.destroy)
button_exit.pack()

# Start the main loop
window.mainloop()


# Define the `rename_model` and `show_model_info` functions:
def rename_model():
    # Get the current model name and proposed new name
    model_name = entry_model_name.get()
    new_name = propose_new_name(model_name)
    
"""
Confirm the rename using a messagebox.askyesno dialog. If the user confirms, the rename_model_files function is called to rename the model files, and the update_model_info function is called to update the model information in the database. Finally, a message is displayed using messagebox.showinfo to inform the user that the model has been renamed.
"""

    # Ask the user to confirm the rename
    message = f"Rename {model_name} to {new_name}?"
    response = messagebox.askyesno(message)
    
    # Rename the model if the user confirms
    if response:
        rename_model_files(model_name, new_name)
        update_model_info(model_name, new_name)
        messagebox.showinfo("Model renamed", f"{model_name} has been renamed to {new_name}")
    else:
        messagebox.showinfo("Model not renamed", f"{model_name} has not been renamed")
 
# Rename the model files
def rename_model_files(old_name, new_name):
    # Rename the model files
    for filename in os.listdir("models"):
        if filename.startswith(old_name):
            new_filename = filename.replace(old_name, new_name)
            os.rename("models/" + filename, "models/" + new_filename)
            
# Update the model information file
def update_model_info(old_name, new_name):
    # Open the model information file
    with open("models.json") as f:
        data = json.load(f)
    
    # Find the model with the old name
    for model in data["models"]:
        if model["name"] == old_name:
            # Update the model's name
            model["name"] = new_name
    
    # Save the updated model information to the file
    with open("models.json", "w") as f:
        json.dump(data, f, indent=4)
        

# Rename the model files and update the information file.
rename_model("old_name", "new_name")    

def rename_model(old_name, new_name):
    # Rename the model file
    old_file = "models/" + old_name + ".json"
    new_file = "models/" + new_name + ".json"
    os.rename(old_file, new_file)
    
    # Update the model information in the database
    update_model_info(old_name, new_name)
    
# Rename a model
rename_model("old_name", "new_name")


# old code to be integrated with new modules-------------------------------------------------



def strip_extension(file_name):
    """
    Strips the extension from a file name if it is of class ModelFile.

    Parameters:
    - file_name (str): The file name to process.

    Returns:
    - base_name (str): The base name (file name without extension).
    """
    model_file = ModelFile(file_name)

    if model_file.is_supported():
        base_name, _ = os.path.splitext(file_name)
        return base_name
    else:
        print(f"Unsupported file type: {file_name}")
        return None

def get_file_list():
    model_list = []  # Initialize an empty list to store model instances

    # Ask the user to select a folder or file
    file_selection = filedialog.askopenfilename(
        title="Select a Model or Folder",
        filetypes=[("Model Files", ModelFiles.extensions)],
    )

    # Check if a file or folder was selected
    if file_selection:
        if is_directory(file_selection):
            print(f"Selected folder: {file_selection}")
            # Process folder
            # Add all files from the folder to model_list
            model_list.extend(add_files_from_folder(file_selection))
        else:
            print(f"Selected file: {file_selection}")
            # Process file
            # Add the selected file to model_list
            model_list.append(ModelFiles(file_selection))

        # Now model_list contains instances of ModelFiles based on user selection
        print("Model List:", model_list)
    else:
        print("No selection made.")

def is_directory(path):
    try:
        # Try to check if the path is a directory
        return os.path.isdir(path)
    except OSError:
        return False

def add_files_from_folder(folder_path):
    files_list = []

    # Walk through the folder and add each file to the list
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if ModelFiles.is_valid(file_path):  # You might need to define a method in ModelFiles to check if the file is valid
                files_list.append(ModelFiles(file_path))

    return files_list


def get_sha256(file_path, chunk_size=8192):
    sha256_hash = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            sha256_hash.update(chunk)
        print(f"SHA-256 Hash for {file_path}: {sha256_hash}")
    return sha256_hash.hexdigest()


def get_model_by_hash(api_url, hash_value):
    endpoint = f"{api_url}/api/v1/model-versions/by-hash/{hash_value}"

    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an error for unsuccessful responses

        model_data = response.json()

        # Save the JSON data to a file
        with open(f"{base_name}.civitai.info", 'w') as json_file:

            json.dump(model_data, json_file, indent=2)

        return model_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    # Get model_info from civitai.info file.
    # If no civitai.info file or missing fields, fetch model_info by hash search from civitai.com
    api_url = "https://civitai.com"
    hash_value = get_sha256(file_path)
    model_data = get_model_by_hash(api_url, hash_value)
    if model_data:
        print("Model Found! Model Data saved to {base_name}.civitai.info")
    else:
        print("Model not found or an error occurred.")


def fetch_creator_username(html_url):
    print("Fetching Author Name from Web...")
    try:
        response = requests.get(html_url)
        response.raise_for_status()
        html_content = response.text
        author_match = re.search(r'"author":"([^"]+)"', html_content)
        return author_match.group(1) if author_match else None
    except requests.RequestException as e:
        print(f"Error fetching HTML content: {str(e)}")
        return None


def extract_model_info(info_path):
    print("Reading civitai.info file...")
    try:
        # TODO: Get title from model page, add option to use the title rather than the model name
        with open(info_path, "r", encoding="utf-8") as info_file:
            info_data = json.load(info_file)
            model_name = info_data.get("model", {}).get("name")
            print(f"model_name: {model_name}")
            model_id = str(info_data.get("modelId", ""))
            print(f"model_id= {model_id}")
            modelVersions_id = str(info_data.get("id", ""))
            print(f"modelVersions_id: {modelVersions_id}")
            modelVersions_name = info_data.get("name", "")
            print(f"modelVersions_name: {modelVersions_name}")
            return model_name, model_id, modelVersions_id, modelVersions_name
    except FileNotFoundError:
        # TODO: Calculate hash and find the file by search
        return None, None, None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {info_path}: {str(e)}")
        return None, None, None, None


def rename_file(folder_path, old_file_name, base_name, new_name):
    old_path = os.path.join(folder_path, old_file_name)
    new_path = os.path.join(
        folder_path,
        re.sub(
            re.escape(base_name),
            new_name,
            old_file_name))
    os.rename(old_path, new_path)
    print(f"Renamed {old_path} ==> {new_path}")


def batch_rename_files(folder_path, base_name, new_name):
    batch_pattern = re.compile(
        fr"{re.escape(base_name)}\.(civitai\.info|preview\.(png|webp|jpg)|safetensors|pt|json)$")
    for search_file_name in os.listdir(folder_path):
        if batch_pattern.match(search_file_name):
            rename_file(folder_path, search_file_name, base_name, new_name)


def rename_folder(selected_file):
    folder_path = os.path.dirname(selected_file)

    # Print the folder path and selected file for debugging
    print(f"Folder Path: {folder_path}")
    print(f"Selected File: {selected_file}")

    base_name = os.path.splitext(os.path.basename(selected_file))[0]

    # Extract model name, modelId, versionId, and version name
    model_name, model_id, modelVersions_id, modelVersions_name = extract_model_info(
        selected_file)

    # Construct the HTML file URL
    html_url = f"https://civitai.com/models/{model_id}?modelVersionId={modelVersions_id}"

    # Fetch author name
    creator_username = fetch_creator_username(html_url)

    if creator_username is None:
        creator_username = "unknown"
        return


def is_valid_filename(filename):
    # Define a regular expression pattern for valid Windows filenames
    valid_filename_pattern = re.compile(r'[^<>:"/\\|?*]')

    # Check if the filename contains any illegal characters
    if valid_filename_pattern.match(filename):
        return True
    else:
        return False

def display_gui(base_name, new_name, model_name, modelVersions_name, creator_username):
    root = tk.Tk()
    root.title("Semi-automatic Model Renamer")

    label_base_name = tk.Label(root, text=f"Base Name: {base_name}")
    label_base_name.pack()

    label_new_name = tk.Label(root, text=f"New Name: {new_name}")
    label_new_name.pack()

    label_model_name = tk.Label(root, text=f"Model Name: {model_name}")
    label_model_name.pack()

    label_modelVersions_name = tk.Label(root, text=f"Version Name: {modelVersions_name}")
    label_modelVersions_name.pack()

    label_creator_username = tk.Label(root, text=f"Author Name: {creator_username}")
    label_creator_username.pack()

    button_model_name = tk.Button(root, text="Edit Model Name", command=edit_model_name)
    button_model_name.pack()

    button_creator_username = tk.Button(root, text="Edit Author Name", command=edit_creator_username)
    button_creator_username.pack()

    button_version = tk.Button(root, text="Edit Version", command=edit_version)
    button_version.pack()

    button_skip_model = tk.Button(root, text="Skip this Model", command=skip_model)
    button_skip_model.pack()

    button_confirm_rename = tk.Button(root, text="Confirm and Rename this Model", command=confirm_rename)
    button_confirm_rename.pack()

    root.mainloop()

    user_input = display_gui(base_name, new_name, model_name, modelVersions_name, creator_username)

    root.destroy()  # Close the GUI after getting user input

    return user_input


def edit_model_name():
    user_input.set("Edit Model Name")
    instring = input("Input new Model Name: ")
    if not valid_filename_pattern.match(instring):
        print("Please refrain from using the FORBIDDEN CHARACTERS: \' [ ^ < > : \" / \\ | ? * ]")
        else:
        model_name = instring


def edit_creator_username():
    user_input.set("Edit Author Name")
    instring = input("Input new Author Name: ")
    if not valid_filename_pattern.match(instring):
        print("Please refrain from using the FORBIDDEN CHARACTERS: \' [ ^ < > : \" / \\ | ? * ]")
        else:
        creator_username = instring


def edit_version():
    user_input.set("Edit Version")
    instring = input("Input new Model Version: ")
    if not valid_filename_pattern.match(instring):
        print("Please refrain from using the FORBIDDEN CHARACTERS: \' [ ^ < > : \" / \\ | ? * ]")
        else:
        modelVersions_name = instring


def skip_model():
    user_input.set("Skip this Model")
    print("Skipped renaming.")


def confirm_rename():
    user_input.set("Confirm and Rename this Model")
    # Rename the file
    new_name = f"{model_name}_by_{creator_username}.{modelVersions_name}"
    rename_file(folder_path, file_name, base_name, new_name)
    print(f"Renamed {old_path} ==> {new_path}")
    last_base_name = base_name

# Main loop
#
# Draw window
#
# Select files or Quit?
while user_input.lower() != "q"
    user_input = input("[S]elect files to rename or [Q]uit?")
    if user_input.lower = "s":
        get_file_selection ()

#
root = tk.Tk()
root.title("Semi-automatic Model Renamer")
user_input = display_gui(base_name, new_name, model_name, modelVersions_name, creator_username)
user_input = tk.StringVar(root)

label_base_name = tk.Label(root, text=f"Original Name: {base_name}")
label_base_name.pack()

label_new_name = tk.Label(root, text=f"New Name: {new_name}")
label_new_name.pack()

label_model_name = tk.Label(root, text=f"Name: {model_name}")
label_model_name.pack()

label_modelVersions_name = tk.Label(root, text=f"Version: {modelVersions_name}")
label_modelVersions_name.pack()

label_creator_username = tk.Label(root, text=f"Author: {creator_username}")
label_creator_username.pack()

button_model_name = tk.Button(root, text="Edit Model Name", command=edit_model_name)
button_model_name.pack()

button_creator_username = tk.Button(root, text="Edit Author Name", command=edit_creator_username)
button_creator_username.pack()

button_version = tk.Button(root, text="Edit Version", command=edit_version)
button_version.pack()

button_skip_model = tk.Button(root, text="Skip this Model", command=skip_model)
button_skip_model.pack()

button_confirm_rename = tk.Button(root, text="Confirm and Rename this Model", command=confirm_rename)
button_confirm_rename.pack()

root.mainloop()

# Access user_input.get() after the GUI closes to get the user's choice
print(f"User Input: {user_input.get()}")

# Define the pattern for matching model files.
file_pattern = re.compile(
    fr"{re.escape(base_name)}\.(civitai\.info|preview\.(png|webp|jpg)|safetensors|pt|json)$")

# Use the file_pattern to check if there are any more files pending processing
matching_file = None
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if file_pattern.match(file_name):
        matching_file = file_name
        break

# Check for matching files
if matching_file is not None:
    # Set the default new name and check if it is a legal Windows filename
    default_name = f"{model_name}_by_{creator_username}.{modelVersions_name}"
    if is_valid_filename(default_name):
        new_name = default_name
    else:
        new_name = base_name

    # Display Proposed change
    print(f"\nCurrent Filename: {matching_file}")
    print(f"Proposed Filename: {new_name}")

    # Use a regular expression to match files with the same base name
    file_pattern = re.compile(
        fr"{re.escape(base_name)}\.(civitai\.info|preview\.(png|webp|jpg)|safetensors|pt|json)$")

    for file_name in os.listdir(folder_path):
        # Display the current and proposed names
        print(f"\nCurrent Name: {file_name}")
        print(f"\nModel Name: {model_name}")
        print(f"Version: {modelVersions_name}")
        print(f"Author Name: {creator_username}")

        # Get user_input != []

    else:
        print("No matching files found.")

if __name__ == "__main__":
    while True:
        root = tk.Tk()
        root.withdraw()  # Hide the main window


# Ask the user if they want to continue
another_job = input("Do you want to perform another job? (y/n): ")
if another_job.lower() != "y":
    print("Exiting.")
    break
