# Project: sd-FileRAVEN

### (Reader-friendly Application for Validated Entity Naming)

Developed by Brian Conroy
<br>Date of initial commit: December 15, 2023

**sd-FileRAVEN** is a cross-platform utility designed to assist users in
quickly and effectively annotating and attributing models with information
about base model, author, and version. By retrieving information for models
downloaded from civitai.com and renaming the model files to user-friendly
standardized filenames, sd-FileRAVEN helps to eliminate duplicates, prevent
confusion between similarly or cryptically named models, enhances
organization, and streamlines the user's model library. With its ability to
help eliminate duplicates and to distinguish identically-named models, this
application proves to be an invaluable asset for model management.
---

## PROJECT MAP / TOC

#### project/

1. fileRAVEN.bat
2. main.py         (Model renaming logic)
3. ui.py           (User Interface)
4. fileRAVEN.config
5. remote_db.json (API info for remote information source databases)
6. keyring.json (encrypted api keys)
6. templates/      (HTML templates for displaying model info)  
   6.1 base.html  
   6.2 model.html
7. readme.md
8. fileRAVEN_Developer's_Reference.md (This document)

---

### 1. fileRAVEN.bat

fileRAVEN.bat is a simple batch program to check/install dependencies, set
launch options and start main.py.

#### 1.1. Default Script

#### 1.2. Launch Options

#### TODO:

- Make default script
- default launch configuration
- enumerate config options
- list dependencies

---

### 2. main.py

main.py controls program flow, data flow, and performs all logical
operations and checks.

#### 1.0. Program flow

#### 1.1. Imports

#### 1.2. Classes

#### 1.3. Constants

#### 1.4. Functions

#### 1.5. Variables

#### TODO:

- Finish second draft flowchart
- pseudocode
- tests
- fill in pseudocode

---

### 3. ui.py

ui.py handles the user interface, windows, human input and display output
(but not disk operations or api calls)

#### 1.0. Program flow

#### 1.1. Imports

#### 1.2. Classes

#### 1.3. Constants

#### 1.4. Functions

#### 1.5. Variables

#### TODO:

- Finish second draft flowchart
- pseudocode
- tests
- fill in pseudocode

---

### 4. fileRAVEN.config

#### 1.0. tags

#### 1.1. default values

#### 1.2. options

#### 1.3. default config file

#### TODO: all

---

### 5. remote_db.json

#### 1. adding databases

Databases are added through the manage databases dialogue. (Main
Menu-->Manage Databases-->Add Remote Database) The first will be
prepopulated for civitai.com. The url will be hashed and the hash will serve
as the dbase_id for that database.
> 'dbase_id': <dbase_id>,<br>
> 'base_url': <https://civitai.com/api/v1/models>
> 'api_key_author': 'username'
> 'api_key_name': 'query'<br>
> 'api_search_by_author': "
>
TODO: Followup and complete civitai.com api configuration
> 'api_search_by_hash': "GET /api/v1/models?hash={hash_value}"<br>
> 'api_key_
> search_hash-256': ''
> search_hash-crc32: ''
> import requests

base_url = "https://api.civitai.co/api/v1/models"
query_params = {
"user": "WhiteRavenCou'atl"
}

response = requests.get(base_url, params=query_params)

# Process the response here

>

#### 2. equivalent variables

#### 3. default values

#### 4. options

#### TODO: all

* Figure out how to add new database api data programatically. Probably
  manually through a configuration window.
  <br>*Note to self: if there's no API it's not my problem. I'm not doing custom
  code for every website out there hosting models. Don't make this harder
  than it has to be.*

---

### 6. keyring.json

##### 1. Format

For each remote source, a key will be added to the ring with a number equal
to the source's id number in the local installation. The key will then be
encrypted using a basic method and stored with it's key.

##### 2. Encryption

---

### 8. Developer's Reference

8.1 Default Naming Templates with notes on strategies
8.2 Launch Options
8.3 Model Identification

#### 1. Default naming strategies:

    *. General
        +. Limit filenames to a set of (mostly) universally acceptable characters:
            -. Lowercase letters
            -. Uppercase letters
            -. Numbers (0-9)
            -. Special characters (underscore, hyphen, period), parenthesis,
            brackets, braces
            -. Generally compatible characters (i.e. (parenthesis), [brackets], and
		    braces
		    the user is issued a permanently skippable (session) warning before file-names are changed in the filesystemrenaming
		    operations are performed:

			**Heads up!**
			

		Using parentheses (()), brackets ([]), or braces ({}) in filenames
		can lead to compatibility issues on some systems or with certain software.
	
		*. ** FAT32 Restriction: ** These characters aren't allowed on FAT32 file
		systems, common on older Windows systems and portable drives.
		*. ** Software Quirks: ** Some older software or scripts might not handle them
		correctly, causing problems.
		*. ** Web Compatibility: ** Some web servers or applications might have
		restrictions on these characters in filenames.

		To ensure maximum compatibility, stick to letters, numbers, underscores (_),
		periods (.), and hyphens (-).

			f. Spaces: Issue a brief, permanently skippable warning:

	Warning: While some systems allow spaces in filenames,
	they can lead to problems on others (older Windows, 
	web servers, etc.). 
			
	** Consider using hyphens (-) instead for universal compatibility. **

        2. For filename elements (e.g. model_name, version_name, etc.), Strip the elements of any forbidden characters (use a class to define letters allowed and loop through the string adding only allowed characters) before adding them to the proposed new filename
        3. Model types: [(Checkpoint, TextualInversion, Hypernetwork, AestheticGradient, LORA, Controlnet, Poses]
            a. Model type default strategies for base_name:
                1. checkpoints:
                    ◦ default format: {title}_by_{creator_name}.{model_style}.{base_model}.{version_name}
                    ▪ title:  the title from the model page. I have found that this is usually a much more descriptive and accurate name than the filename given.
                    ▪ creator_name:  the name of the creator of the model.
                    ▪ model_style:  the style of the model. Start with these categories and refine after testing and feedback:
                        • photo: photo-realistic models
                        • multi: general purpose models. Models not tuned to specific output types, or tuned to multiple types, e.g. SD1.5 base-model
                        • art: Non-photo-realistic artistic styles
                        • trad: Traditional media styles (e.g., oilpaint, watercolor, sketch)
                        • cgi3d: Computer-generated 3D styles (e.g., Pixar, Unreal Engine)
                        • abst: Abstract imagery"line": line-arts (e.g. anime, manga, sketch, charcoal, western traditional animation, comic book, cell-shaded, etc) style art
                ◦ LoRAs, TI’s, and Hypernetworks
                    ▪ Check model tags for keywords indicating the model represents a character, person, or celebrity, etc.
                    ▪ If the model has a tag that matches any of these keywords, the model is a character. Check to see if it represents a real person
                        • check the "resembles_real_person" flag in the API response, if "true" exit the check loop.
                        • If the model tags include any of [influencer, celebrity, actor, actress, instagram, tiktok, pornstar, singer, adult model] set the "resembles_real_person flag to true and exit the check loop
                        • Look for "not a real person", "not real", "cartoon", "anime", "hentai", "game", "rpg", or "fictional character" in the title and text of the model page.
                        • If model tags include any of [fictional, ai character, anime, not real, cartoon, anime, hentai, game, rpg, etc.] set the "resembles_real_person flag to false and exit the check loop "
                        • if any of the above return positive:
                            ◦ break out of the check loop and set the "resembles_real_person" flag to "false"
                            ◦ record the flag in the civitai.info file
                            ◦ else set the "resembles_real_person" flag to true and record the value in the civitai.info file.
                            ◦ give the user the option to change the flag before renaming the model.
                            ◦ If "resembles_real_person" != "false" then real_tag = "true"
                            ▪ Note: Trap the possibility of an empty flag and default to "true"
                        ◦ LoRAs and Hypernetworks:
                            ▪ Character:
                                • {Character_name}_of_{title}_portrayed_by_{actor}_by_<content_>
                        ◦ Textual Inversions:

        Information to extract from Civitai/Remote db:
            - id                    number      The identifier for the model
            - name                  string      The name of the model
            - type                  enum        The model type (Checkpoint,
                                                TextualInversion, Hypernetwork,
                                                AestheticGradient, LORA,
                                                Controlnet, Poses)
            - nsfw                  boolean     NSFW flag
            - tags                  list        A list of tags associated with
                                                the model
            - creator.username      string      The name of the creator
            - modelVersions.id      number      The identifier for the model version
            - modelVersions.name    string      The name of the model version
            - modelVersions.files.  enumerated  The specified floating point for
                metadata.fp                     the file (fp16, fp32, undefined)
            - modelVersions.files.  enumerated  The specified model size for the
                metadata.size                   file (full, pruned, or undefined)
            - modelVersions.images. string	    The id for the image
                id
            - modelVersions.images. string	    The url for the image
                url
            - modelVersions.images. number	    The original width of the image
                width
            - modelVersions.images. number	    The original height of the image
                height

2. Launch Options
3. Model Identification
   If the model does not have a model-page stored in its <model>.info file,
   <model>.civitai.info, or <model>.json files fileRAVEN will search through
   its remote databases until it finds a model-page. As it stands, it makes
   sense to hard-code civitai.com and huggingface.co. but as there are
   others out there, and surely others will emerge, fileRAVEN should not be
   limited by them. The search will begin with a search by crc32 in civitai.
   com. If the crc32 search has no returns, or multiple returns, the program
   will perform an sha-256 search of civitai.com. If both hash searches
   produce no matches, search by known information
