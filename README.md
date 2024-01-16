# sd-FileRAVEN (Reader-friendly Application for Validated Entity Naming)

## **Status: Very Early development (contributions welcome!)**
### Note: I am very new to Python and to managing a Github project. Please be patient for I have only half a clue!

Organize &amp; manage your Civitai models! sd-FileRAVEN cleans duplicates, standardizes filenames, adds author &amp; version info, making your library neat &amp; easy to navigate. Ditch confusing names &amp; say goodbye to model chaos!

**Author: WhiteRaven-Cou'atl**

## Introduction:
sd-FileRAVEN is a cross-platform utility for managing Stable Diffusion models. It tackles the pain points of confusing filenames, missing information, and duplicate downloads. Imagine a tidy library where models are clearly named, attributed, and organized for seamless workflow. That's what sd-FileRAVEN strives for.

## Current Development Features:
- Standalone program works with any user interface/s you use!
- Developed with Python 3.10.6 for stability and cross-platform compatibility with sd-webui.
- Automatically annotates and renames files: Retrieves model information from civitai.com and standardizes filenames to include model name, author, version, and base model for easy identification.
- The Civitai Model Page is displayed, allowing the user to verify accuracy and make informed decisions regarding renaming.
- Automatically renames all associated files (.civitai.info; .preview.png; etc.).
- Automatic cross-version renaming: Optionally detect and rename different versions of the same model with matching names automatically.
- Simplifies organization and enhances searchability for efficient access.
- Shares .civitai.info files with sd-webui-Civitai-Helper to prevent creating file clutter
- Identifies models previously processed by FileRAVEN

* Mark LoRAs and embeddings of real people to easily distinguish them from
  fictional characters.
* Identify and separate LyCORIS files from LoRA files. Append .lyco or .lora
  to filename by default
* Identify and append .ti to filenames for safetensors embeddings by default

## Future Features:

* Full MySQL database and management "sd-fileRAVEN-librarian" branch
    * Import all models to a common file location and automatically set
      symlinks to stable diffusion programs when they are set up in sd-fileRAVEN
* Browsable database with source links and thumbnails
- Automatic preview image download
- Provide customizable naming formulas for different model types (e.g. checkpoint merges & base models; LoRAs; textual inversions, etc.).
- Use ai enhanced search to improve detection of real people embeddings and
  LoRA models
- Mark models according to license so that you know whether you can use it for your commercial project or not!
- Sort models into appropriate folders based on customizable tags. Imagine downloading a hundred LoRAs, TI's, and checkpoints, and moments later they are renamed and sorted into the correct folders on your PC ready for use.
- Removes duplicate downloads for a streamlined library.
- Integrations: Planned branches for sd-webui extension and potential
  ComfyUI integration + others

* Support/Integration for Model Templates
## Current Features Under Development:

- Developed using Python 3.10 to ensure stability and cross-platform
  compatibility with sd-webui.
- Automatically annotates and renames files: Retrieves model information from civitai.com and standardizes filenames to include model name, author, version, and base model for easy identification.
- Users have the opportunity to fine-tune the name before renaming occurs.
- Automatically renames all associated files (.civitai.info; .preview.png; etc.).
- Automatic cross-version renaming: Optionally rename different versions of the same model with matching names automatically.
- Simplifies organization and enhances searchability for efficient access.
- Differentiate embeddings from other model types to avoid the use of spaces or underscores, ensuring a readable TI that will not be misinterpreted by CLIP.

## Future features:
- Provide customizable naming formulae for different model types (e.g. checkpoint merges & base models; LoRAs; textual inversions, etc.).
- Automatically mark LoRAs and embeddings of real people to distinguish them from fictional characters
- Automatically mark models based on their licenses to help the user determine if they can be used for commercial projects.
- Sort models into appropriate folders based on customizable tags.
- Remove duplicate downloads for a streamlined library.
- Form a model database to easily manage and locate local files.
- Integrations: Planned forks for sd-webui extension and potential ComfyUI integration.

## Utilizes:
- Python 3.10.6
- gradio-app by gradio: https://github.com/gradio-app/gradio
- REST API by civitai: https://github.com/civitai/civitai/wiki/REST-API-Reference

## Why build this?
As an avid enthusiast of Stable Diffusion, I quickly encountered challenges while navigating my expanding library of LoRAs with default model names. Distinguishing between similarly named models and preventing the proliferation of duplicate copies became increasingly difficult. Moreover, I found it challenging to recall the significance of certain files, such as "fg00074000009e4.safetensors." I yearned for standardized and more human-readable names to streamline the process.

To address this, I began to standardize my model names when downloading new models, incorporating more descriptive and helpful information. For example, instead of accepting the default filename, "gBushv25.safetensors", I would look at the model page and create a standardized formulaic name like "George_Bush_by_MrAwesome.politician.REAL.v2.5.SDXL.safetensors." This new system made it easy for me to see key information at a glance. What is the subject of this model? Who made it? Is this a real or fictional person? Is this for SD 1.5 or SDXL? Which version is it? The enhanced clarity provided by the new filenames significantly improved my ability to quickly and accurately locate the right LoRA or model. However, it also made the process of downloading models more tedious and time-consuming. Additionally, I realized that I would need to individually fix each file in my existing library, a task even more time-consuming than making the changes during the download. I had been utilizing butaixianran's [Stable-Diffusion-Webui-Civitai-Helper.](https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper)
(Great project, extremely useful! I'm a big fan!). This meant that for each file, there was also a preview image, JSON file, and civitai.info file that needed renaming. With a library of nearly 4,000 models, it was indeed a daunting task!

Inspired by Civitai-Helper and motivated by the desire to streamline my process and to begin learning Python, I decided to address both of my issues simultaneously. I embarked on creating a program that would not only tackle my own organizational challenges but also serve as a learning platform for me to learn Python. Thus, sd-FileRAVEN was born.

As I refined my project plan, my initial vision for sd-FileRAVEN, once confined to renaming, took flight. It soared to new heights as I reconceptualized it as a versatile and robust model-management application. This is a bit of an extreme challenge for a beginner programmer, but I believe that, with the support of the open-source community (as well as crash-course learning and intensive tutoring by Llama 2), the dream of fileRAVEN can be achieved. My goal is to create a comprehensive solution that will tackle the various model-management obstacles faced by Stable Diffusion users. I am certain that sd-FileRAVEN will become an indispensible asset for individuals looking for improved organization and clarity within their model library.

In summary, sd-FileRAVEN represents my commitment to not only resolving my personal challenges but also contributing to the broader community of Stable Diffusion enthusiasts by providing a robust and versatile solution.

## TLDR
Cross-platform utility for Stable Diffusion! sd-FileRAVEN auto-renames models with author, version, & base model info, simplifies organization, and removes duplicates. Built with Python 3.10 for cross-platform compatibility and sd-webui integration.

## Contributions & Feedback:
I'm actively seeking feedback and contributions to shape sd-FileRAVEN into a robust and user-friendly tool. Feel free to open issues, pull requests, or simply share your thoughts. Let's build a better model management solution together!
