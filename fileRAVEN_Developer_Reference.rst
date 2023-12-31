=================================================================================
Project: sd-FileRAVEN (Reader-friendly Application for Validated Entity Naming)
=================================================================================

Developed by Brian Conroy
Date of initial commit: December 15, 2023

sd-FileRAVEN is a cross-platform utility designed to assist users in quickly and
effectively annotating and attributing models with information about base model,
author, and version. By retrieving information for models downloaded from
civitai.com and renaming the model files to user-friendly standardized filenames,
sd-FileRAVEN helps to eliminate duplicates, prevent confusion between similarly
or cryptically named models, enhances organization, and streamlines the user's
model library. With its ability to help eliminate duplicates and to distinguish
identically-named models, this application proves to be an invaluable asset for
model management.

======================
PROJECT MAP

    project/
        ├── main.py         (Model renaming logic)
        ├── ui.py           (User Interface)
        ├── civitai.json    (CivitAI API info)
        ├── templates/      (HTML templates for displaying model info)
        ├── base.html
        ├── model.html
        ├── readme.md
        └── fileRAVEN.rst (This document)

----------------------------
Default naming strategies:

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

			Heads up!
			---------

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
