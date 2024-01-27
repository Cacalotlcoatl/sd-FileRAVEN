import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, WARNING


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("fileRAVEN-Lite")
        self.master.geometry("400x300")

        # Draw the main menu
        self.render_main_menu()

    def render_main_menu(self):
        menu_frame = tk.Frame(self.master)
        menu_frame.pack(pady=100)

        select_model_button = tk.Button(menu_frame,
                                        text="Select Model/s or Folder",
                                        command=self.on_select_model_click)
        select_model_button.pack(pady=10)

        edit_naming_button = tk.Button(menu_frame, text="Edit Naming Schemes",
                                       command=self.on_edit_naming_click)
        edit_naming_button.pack(pady=10)

        quit_button = tk.Button(menu_frame, text="Quit to Desktop",
                                command=self.master.quit)
        quit_button.pack(pady=10)

    def on_select_model_click(self):
        file_path = filedialog.askopenfilename(initialdir="/",
                                               title="Select SD_model file",
                                               filetypes=(("SAFETENSORS files",
                                                           "*.safetensors"),
                                                          ("Checkpoint files",
                                                           "*.ckpt"),
                                                          ("Binary files",
                                                           "*.bin"),
                                                          ("PyTorch files",
                                                           "*.pt")))
        print("Selected file:", file_path)

    def on_edit_naming_click(self):
        # Add logic for naming scheme editor
        print("Edit Naming Scheme Editor button clicked")


class SdModels:
    def __init__(self, master):
        self.master = master
        self.master.title("File Selection")
        self.master.geometry("400x200")

        # Create a button to open the file picker
        pick_button = tk.Button(self.master, text="Pick File",
                                command=self.pick_file)
        pick_button.pack(pady=20)

    def pick_file(self):
        file_path = filedialog.askopenfilename(initialdir="/",
                                               title="Select SD_model file",
                                               filetypes=(("SAFETENSORS files",
                                                           "*.safetensors"), (
                                                              "Checkpoint "
                                                              "files",
                                                              "*.ckpt"), (
                                                              "Binary files",
                                                              "*.bin"), (
                                                              "PyTorch files",
                                                              "*.pt")))
        print("Selected file:", file_path)


# General purpose interactive function
def ask_ok(aoktitle, aokprompt, ok_button_text, cancel_button_text,
           aok_success_text
           ):
    # create the root window
    root = tk.Tk()
    root.title(aoktitle)
    root.geometry('300x150')

    # click event handler

    answer = askokcancel(
        title=aoktitle,
        message=askokprompt,
        icon=WARNING)

    if answer:
        showinfo(
            title=aoktitle,
            message=(aok_success_text)

        ttk.Button(
            root,
            text='',
            (command=confirm).pack(expand=True)

        # start the app
        root.mainloop()

#
# ------------------------------------------------------------------------------

# Initialize the GUI
root = tk.Tk()
app = GUI(root)

# Run the main loop to keep the window open
root.mainloop()
