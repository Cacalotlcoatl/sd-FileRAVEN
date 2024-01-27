import streamlit as st


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
        select_model_button = st.button("Select Model/s or Folder")
        if select_model_button:
            self.on_select_model_click()

        edit_naming_button = st.button("Edit Naming Schemes")
        if edit_naming_button:
            self.on_edit_naming_click()

        quit_button = st.button("Quit to Desktop")
        if quit_button:
            st.stop()

    def on_select_model_click(self):
        """
        Function to handle the click event for selecting a model. It prompts
        the user to upload
        a specific type of file and then displays the selected file.
        """
        file_path = st.file_uploader("Select SD_model file",
                                     type=["safetensors", "ckpt", "bin", "pt"])
        if file_path:
            st.write("Selected file:", file_path)

    def on_edit_naming_click(self):
        """
        Add logic for naming scheme editor
        """
        st.write("Edit Naming Scheme Editor button clicked")


# Initialize the Streamlit app
gui = GUI()
