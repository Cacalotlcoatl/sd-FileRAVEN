# sd-fileRAVEN (Reader-friendly Application for Validated Entity Naming)

## **Status: Suspended Pre-Alpha Early development (contributions welcome!)**
### I have suspended this project briefly while I achieve some of my education goals. Don't worry, I'll be back soon and get this project on-track!

### Note: As a newcomer to software development, this project is my personal endeavor to learn Python programming and project management fundamentals. I am aware that I have much to learn, and am open to criticism. Your patience and understanding are greatly appreciated as I embark on this learning journey. Contributions from experienced developers or enthusiasts are warmly welcomed and will help shape the project's growth and success. Together, let's create something remarkable.

### **Author: WhiteRaven-Cou'atl**

### Organize &amp; manage your Civitai models! sd-fileRAVEN cleans duplicates, standardizes filenames, adds author &amp; version info, making your library neat &amp; easy to navigate. Ditch confusing names &amp; say goodbye to model chaos!

## Vision:
### sd-fileRAVEN is a cross-platform utility for managing Stable Diffusion models. It tackles the pain points of confusing filenames, missing information, and duplicate downloads. Imagine a tidy library where models are clearly named, attributed, and organized for seamless workflow. That's what sd-fileRAVEN strives for.

## Initial Feature Set for Development:
- **Standalone Program**: works with any user interface/s you use!
- **Stable Python Release**:Developed with Python 3.12.1 for stability and cross-platform compatibility.
- **Automatically Annotate and Rename Models**: Retrieves model information from CivitAI.com and standardizes filenames to include model name, author, version, and base model for easy identification. Rename model files in your language for ease-of use (English support only in initial release)
- **Customizable Naming Formulae**: Allow users to define naming formulas specific to different model types (e.g., checkpoint merges, LoRAs, textual inversions) for better organization and clarity.
- **Review/preview Model Information Pages**: Information from the CivitAI Model Page is displayed, allowing the user to verify accuracy and make informed decisions regarding renaming.
- **Cluster Renaming**: Automatically renames all associated files (.civitai.info; .preview.png; etc.) Users have the opportunity to fine-tune the name before renaming occurs.
- **Automatic Cross-Version Renaming**: Optionally detect and rename different versions of the same model or members of a model collection with matching name patterns automatically.
- **Standardizes and Simplifies**: helps organization and enhances searchability for efficient access.
- **Compatibility**: Shares .civitai.info files compatible with sd-webui-Civitai-Helper to prevent creating additional file clutter and allow interoperability
- **Efficient Model Tracking**: Identify previously processed models to streamline processing and eliminate redundant work in sd-fileRAVEN.
- **Embedding Specific Naming**: Ensure human-readability and function by using embedding-specific naming strategies that avoid spaces or underscores while maintaining triggerword distinctiveness to prevent misinterpretation by CLIP.
- **Model Type Differentiation**: Distinguishes between various model types such as base model checkpoints, LoRAs, Textual Inversions, Hypernetworks, etc. Allowing for model-type specific behavior such as type-specific naming templates and sorting.
- **Automatic Preview Image Download**: Automatically searches for and downloads a thumbnail from civitai.com, if available.

## Future Features:
- **Localisation and Language Adaption**: Localization files tailored for specific languages, and easy AI-assisted name translation ensuring seamless integration with different linguistic contexts.
- **Real Person Marking**: Automatically differentiate and mark LoRAs and embeddings of real people from fictional characters to facilitate easy identification and prevent potential legal or ethical issues associated with using models of real individuals. Initially based on information from the model-page and user-input, but in future, use ai and/or web information to help identify models of real-world people fully automatically.
- **Artist Style Identification**: Identify models that replicate the distinctive art styles of human artists to help users avoid unintentional plagiarism of copyrighted works and maintain ethical standards in their creative endeavors.
- **Use-Rights Permission Flags**: Flag models with specific use-rights permission flags to assist users in preventing unintentional plagiarism or violations of terms-of-use, ensuring that they stay within legal and ethical boundaries when utilizing models in their projects.
- **Sub-Folder Sorting with Customizable Tags**: Sort models into appropriate folders and sub-folders using customizable tags, ensuring a well-organized library and easy access to specific model types.
- **Duplicate Download Prevention and Deduping**: Remove duplicate downloads to maintain a streamlined library and save storage space. Identify subsequent versions of existing models and offer to replace the old model with the new.
- **Automatic Model Updates**: Search for new versions of existing models and automatically download and rename them according to the naming template of the previous version. User choice between keeping or overwriting the old model.
- **Model Database Management**: Create a model database to efficiently manage and locate local files, enhancing overall file organization and retrieval.
- **Customizable Source List**: Provide for full integration of additional user-customizable model sources such as Hugging Face.
- **Automatic Preview Image Generation**: User configures their preferred stable-diffusion UI to automatically generate preview images for models that lack one, utilizing model metadata as a basis for the generated image.
- **Other Paradigms**: Forked projects to handle files and models for other similar software ecosystems.

## Integration Plans: 
Extensions, nodes, plugins, etc. for:
- stable-diffusion webui
- ComfyUI
- Deforum
- Stable Horde
- others

## Utilizes:
- [Python 3.12](https://www.python.org/downloads/release/python-3121/)
- [Streamlit](https://streamlit.io/)
- [Civitai REST API](https://github.com/civitai/civitai/wiki/REST-API-Reference)
- **_For stable-diffusion-webui extension only:_**
    - [gradio:](https://github.com/gradio-app/gradio) gradio-app for UI
    - [Python 3.10.6](https://www.python.org/downloads/release/python-3106/)

## Why build this?
As an avid enthusiast of Stable Diffusion, I quickly encountered challenges while navigating my expanding library of LoRAs with default model names. Distinguishing between similarly named models and preventing the proliferation of duplicate copies became increasingly difficult. Moreover, I found it challenging to recall the significance of certain files, such as "fg00074000009e4.safetensors." I yearned for standardized and more human-readable names to streamline the process.

To address this, I began to standardize my model names when downloading new models, incorporating more descriptive and helpful information. For example, instead of accepting the default filename, "gBushv25.safetensors", I would look at the model page and create a standardized formulaic name like "George_Bush_by_MrAwesome.politician.REAL.v2.5.SDXL.safetensors." This new system made it easy for me to see key information at a glance. What is the subject of this model? Who made it? Is this a real or fictional person? Is this for SD 1.5 or SDXL? Which version is it? The enhanced clarity provided by the new filenames significantly improved my ability to quickly and accurately locate the right LoRA or model. However, it also made the process of downloading models more tedious and time-consuming. Additionally, I realized that I would need to individually fix each file in my existing library, a task even more time-consuming than making the changes during the download. I had been utilizing butaixianran's [Stable-Diffusion-Webui-Civitai-Helper.](https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper)
(Great project, extremely useful! I'm a big fan!). This meant that for each file, there was also a preview image, JSON file, and civitai.info file that needed renaming. With a library of nearly 4,000 models, it was indeed a daunting task!

Inspired by Civitai-Helper and motivated by the desire to streamline my process and to begin learning Python, I decided to address both of my issues simultaneously. I embarked on creating a program that would not only tackle my own organizational challenges but also serve as a learning platform for me to learn Python. Thus, sd-fileRAVEN was born.

As I refined my project plan, my initial vision for sd-fileRAVEN, once confined to renaming, exploded as I reconceptualized the program to be more than just a useful script, but rather a comprehensive, versatile, and robust model-management application. I realize that this project is extremely ambitious, especially for a new developer, but I thrive in a challenge, so let's do this! I believe that, with the support of the open-source community (as well as crash-course learning and ai coding assistants), the dream of sd-fileRAVEN can be achieved. My goal is to create a comprehensive solution that will tackle the various model-management obstacles faced by Stable Diffusion users. I am certain that sd-fileRAVEN will become an indispensible asset for individuals looking for improved organization and clarity within their model library.

In summary, sd-fileRAVEN represents my commitment to not only resolving my personal challenges but also contributing to the broader community of Stable Diffusion enthusiasts by providing a robust and versatile solution.

## TLDR
Cross-platform utility for Stable Diffusion! sd-fileRAVEN auto-renames models with author, version, & base model info, simplifies organization, and removes duplicates. Built with Python 3.10 for cross-platform compatibility and sd-webui integration.

## Contributions & Feedback:
I'm actively seeking feedback and contributions to shape sd-fileRAVEN into a robust and user-friendly tool. Feel free to open issues, pull requests, or simply share your thoughts. Let's build a better model management solution together!
