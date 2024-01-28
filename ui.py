import streamlit as st
import streamlit.components.v1 as components

class GUI:
    def __init__(self):
        """
        Initializes the class instance and sets up the title "fileRAVEN-Lite".
        Renders the main menu.
        """
        st.title("fileRAVEN-Lite")

        # Draw the main menu
        self.render_main_menu()

    def render_main_menu(self):
        """
        Renders the main menu with buttons to select a model or folder, edit
        naming schemes, and quit to desktop.
        """
        select_model_button = st.button("Select Model to Process")
        if select_model_button:
            self.on_select_model_click()

        edit_name_scheme_button = st.button("Edit Naming Schemes")
        if edit_name_scheme_button:
            self.on_edit_name_scheme_click()

        configure_fileraven_button = st.button("Configure fileRAVEN")
        if configure_fileraven_button:
            self.on_configure_fileraven_click()

        quit_button = (
            st.button("Quit "
                      "to Desktop"))
        if quit_button:
            st.stop()

    def on_select_model_click(self):
        """
        Function to handle the click event for selecting a model. It prompts
        the user to upload  a specific type of file and then displays the
        selected file.
        """
        file_path = st.file_uploader("Select SD_model file",
                                     type=["safetensors", "ckpt", "bin", "pt"])
        if file_path:
            st.write("Selected file:", file_path)

    def on_edit_name_scheme_click(self):
        """
        Handle the click event for editing the name scheme.
        Display the naming schemes, the default template for the selected
        scheme, allow the user to edit literals, and display optional
        elements as
        buttons.
        """
        schemes = {
            "Base Model/Checkpoint Merge": "default_template_1",
            "LoRA": "default_template_2",
            "Embeddings": "default_template_3",
            "other/default": "default_template_4"
        }


'''
Display 
    Edit name scheme for LoRA/LyCORIS
        a. LoRA default template
        b. Dropdown menu with Checkboxes for optional templates
            1. Options
                D. (model_title + ' by ' + model_credit + '.' + 
                    model_base_short + '.' + model_version + '.' + nsfw_flag[
                    model_nsfw])
                0. Default: (model_title + ' by ' + model_credit + '.' + 
                    model_base_short + '.' + model_version + '.' + nsfw_flag[
                    model_nsfw])
                1. Action
                2. Art styles
                3. Artist styles
                4. Character
                5. (Real) Person
                6. Expression
                7. Location
                8. Pose
                8. Slider
            2. If a dropdown item is picked, the template for that option is 
            displayed. If the item has not been customized, the default 
            template is displayed. There is a button to reset to default. For 
            menu items >0 it sets the template to template_lora[0]. For option 
            0, it resets to the fileRAVEN default template for LoRAs  

Checkpoint
        b. LoRA/LyCO
                    c. Textual-Inversion
            1. Art styles
            2. Artist styles
            3. Character
            4. (Real) Person
            5. Location
            6. Action
            7. Expression
            8. Negative
        d. Aesthetic Gradient
        e. Hypernetwork
            1. Art styles
            2. Artist styles
            3. Character
            4. (Real) Person
            5. Location
            6. Action
            7. Expression
'''
# Display the naming schemes
selected_scheme = st.sidebar.selectbox("Select a scheme to edit",
                                       list(schemes.keys()))

# Display the default template for the selected scheme
st.write(f"Default template: {schemes[selected_scheme]}")

# Allow the user to click to edit literals
edited_literal = st.text_input("Edit literals here")

# Display optional elements as buttons
optional_elements = ["model_id", "model_name", "model_title",
                     "model_src_name", "model_type", "model_nsfw",
                     "model_real", "model_credit", "model_ver_id",
                     "model_version", "model_fp", "model_base_model",
                     "model_base_model abbrev,", "LoRA/LyCO flag",
                     "model_permit_credit", "model_permit_sell",
                     "model_permit_comgen", "model_permit_civgen",
                     "model_permit_sharemerge",
                     "model_permit_sellmerge",
                     "model_permit_different",
                     "model_collection_name", "model_collection_id",
                     "model_fr_tags", "model_sort_name",
                     "Style_format", "SD_version"
                     ]

'''
  '''
selected_elements = st.multiselect("Select optional elements",
                                   optional_elements)

# Allow the user to rearrange the variables
moved_variable = st.slider("Move variable", min_value=1, max_value=10, value=5)

# Add forward and back arrow controls to move the variable
components.html("<- Back", width=50, height=30)
components.html("Move", width=50, height=30)
components.html("Forward ->", width=50, height=30)
"""
        st.write("Edit Naming Scheme Editor button clicked")


# Initialize the Streamlit app
gui = GUI()

'''
Include in configuration file:
    path list of models
    (future) database path
    language
    theme
    NSFW/SFW flags
    POI flags # POI = Person of Interest, used to denote models depicting real 
    people
    POI failsafe # Boolean, does the user want to default to POI or not?
    Training Model # Use the name of the training model (for
    LoRAs and embeddings) implement later. Unnecessary for now.
    Stable Diffusion Version flags # Distinguish between stable-diffusion 
    versions with these flags, e.g. "SD1", "SDXL", etc.
'''
