import os
import shutil
import tkinter as tk
import keyboard
import time
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

files_destinations = {
    ".mp3": "D:\\Download too\\From Telegram\\Audios",
    ".mp4": "D:\\Download too\\From Telegram\\Videos",
    ".wmv": "D:\\Download too\\From Telegram\\Videos",
    ".mkv": "D:\\Download too\\From Telegram\\Videos",
    ".docx": "D:\\Download too\\From Telegram\\Word files",
    ".doc": "D:\\Download too\\From Telegram\\Word files",
    ".xlsx": "D:\\Download too\\From Telegram\\Excel files",
    ".xls": "D:\\Download too\\From Telegram\\Excel files",
    ".pub": "D:\\Download too\\From Telegram\\Publisher files",
    ".py": "D:\\Download too\\From Telegram\\Source Code files",
    ".c": "D:\\Download too\\From Telegram\\Source Code files",
    ".cpp": "D:\\Download too\\From Telegram\\Source Code files",
    ".pdf": "D:\\Download too\\From Telegram\\PDF",
    ".jpg": "D:\\Download too\\From Telegram\\Pictures",
    ".png": "D:\\Download too\\From Telegram\\Pictures",
    ".gif": "D:\\Download too\\From Telegram\\Pictures",
    ".svg": "D:\\Download too\\From Telegram\\Pictures",
    ".rar": "D:\\Download too\\From Telegram\\Zip files",
    ".zip": "D:\\Download too\\From Telegram\\Zip files",
    ".exe": "D:\\Download too\\From Telegram\\Programs",
    ".msi": "D:\\Download too\\From Telegram\\Programs",
    ".pptx": "D:\\Download too\\From Telegram\\PowerPoint files",
    ".ico": "D:\\Download too\\From Telegram\\Pictures",
    ".psd": "D:\\Download too\\From Telegram\\Photoshop files",
    ".accdb": "D:\\Download too\\From Telegram\\Access Database Files",
}

# Function to get user input from the entry widget
def user_input():
    global myInput
    myInput = entry.get()
# Function to get the user input inside the EDIT tab
def user_edit_input():
    global editInput
    editInput = comboBox.get()

# Function to check if the text box is active or not
def on_focus(event):
    global text_state
    text_state = True
def not_on_focus(event):
    global text_state
    text_state = False
def on_click_outside(event):
    global text_state
    if event.widget != output:  # Check if the click event is not on the Text widget
        text_state = False
# Function to move files from source directory to respective destination directories
def move_files(source):
    global messages
    messages = [] # List to store messages about file move status
    try:
        for files in os.listdir(source):
            file_path = os.path.join(source, files)
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(files)[1].lower()
                if file_extension in new_files_destinations:
                    destinations = new_files_destinations[file_extension]
                    if not os.path.exists(destinations):
                        os.makedirs(destinations)
                    try:
                        shutil.move(file_path,destinations)
                        messages.append("Successfully moved " + files + " to " + destinations)
                    except Exception as e:
                        messages.append("Failed to move " + files + ": " + str(e))
                elif file_extension not in new_files_destinations:
                    other_files_path = f"{saved}:\\Download too\\From Telegram\\Other downloads"
                    if not os.path.exists(other_files_path):
                        os.makedirs(other_files_path)
                    try:
                        shutil.move(file_path, other_files_path)
                        messages.append("Successfully moved " + files + " to " + other_files_path)
                    except Exception as r:
                        messages.append("Failed to move " + files + ": " + str(r))
    except Exception as y:
            time.sleep(1)
            messagebox.showinfo("There is something wrong...","ERROR: (Incorrect directory or doesn't exist!)\n"+ str(y))
            keyboard.add_hotkey('enter', stopKey)
            time.sleep(1)
            
# Function to stop key press event
def stopKey():
    pass                

# Function to ask the user of folder location
def browseFolder():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        entry.delete(0, tk.END)
        entry.insert(0, selected_folder)

# Function to update canvas with messages
def update_canvas(messages):
    for message in enumerate(messages):
        output.configure(state=tk.NORMAL)
        output.delete("1.0", tk.END)
        output.insert("1.0", f"{message}\n")
        output.configure(state=tk.DISABLED)

# Driver letter checking function
def driveChecking():
    driveLetters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    global saved
    saved = editInput

    if saved in driveLetters:
        global new_files_destinations
        new_files_destinations = {
            key: value.replace("D:\\Download too\\From Telegram", f"{saved}:\\Download too\\From Telegram")
            for key, value in files_destinations.items()
        }

# Setting up the main Tkinter window
root = Tk()
root.title("File manager")
root.configure(background="gray")
root.minsize(700,500)

# Styling the tabs
style = ttk.Style()
style.theme_create("MyStyle", parent="alt", settings={
    "TNotebook.Tab": {
        "configure": {"padding": [10, 5], "background": "lightgray"},
        "map": {"background": [("selected", "blue")], "foreground": [("selected", "white")]}
    }
})
style.theme_use("MyStyle")

# Adding labels to the window
text = Label(root, text="\nFile manager made by Sy Sophaneth",bg="gray" , font=("Arial",16))
text.pack()
text2 = Label(root, text="\nA file mover software project\n", bg="gray", font=("Arial",14)).pack()

# Defining the dimensions for the folder location input entry widget
inputWidth = 60
inputHeight = 40

# Defining the state of the text box in the Main tab
text_state = False

# Creating tabs
tabControl = ttk.Notebook(root)
tab1 = tk.Frame(master=None, width=10,height=25)
tab2 = tk.Frame(master=None, width=10,height=25)

tabControl.add(tab1, text="Main")
tabControl.add(tab2, text="Edit")
tabControl.pack(expand=0, fill="both")

# Wrapper function to get user input, move files, and update canvas
def wrap_move_files():
    if tabControl.index(tabControl.select()) != 0 or text_state == True: return
    user_input()
    source = myInput
    move_files(source)
    update_canvas(messages)

# Functions to save modified settings inside "Edit" tab
def wrap_save_settings():
    if tabControl.index(tabControl.select()) != 1: return
    user_edit_input()
    driveChecking()


# Adding widgets to the first tab (Main)
## Text Section
text3 = Label(tab1, text="Please input your folder directory here!", font=("Arial",12)).pack()
text4 = Label(tab1, text=" ").pack()

## Entry section
entry = tk.Entry(tab1,width=inputWidth)
entry.configure(highlightthickness=2,highlightcolor="black")
entry.pack()

## Buttons section
button2 = tk.Button(tab1, text="Browse Folder...", bg="gray", font=("sans-serif", 11), fg="black", command=browseFolder)
button2.pack(padx=20, pady=20)
button = tk.Button(tab1, text="  Move files!  ", bg="blue",font=("sans-serif", 11), fg="white", command=wrap_move_files)
button.pack(padx=20, pady=20)

## Tips and output section
importantText = Label(tab1, text="Please select your disk letter first in the \"Edit\" tab!").pack()
output = tk.Text(tab1, width=70, height=15, state="disabled", highlightcolor="black", highlightthickness=2, wrap=tk.NONE)
output.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

### Vertical scrollbar
vsb = tk.Scrollbar(tab1, orient=tk.VERTICAL, command=output.yview)
vsb.pack(side=tk.RIGHT, fill=tk.Y)
output.configure(yscrollcommand=vsb.set)

### Horizontal scrollbar
hsb = tk.Scrollbar(tab1, orient=tk.HORIZONTAL, command=output.xview)
hsb.pack(side=tk.BOTTOM, fill=tk.X)
output.configure(xscrollcommand=hsb.set)

# Bind functions to the outputs to check if the text box is active 
output.bind("<FocusIn>", on_focus)
output.bind("<FocusOut>", not_on_focus)

# Bind root with function to set the text box to become unactive
root.bind("<Button-1>", on_click_outside)

# Adding widgets to the second tab (Edit)
tab2.grid_columnconfigure(0, weight=1)
tab2.grid_columnconfigure(1, weight=1)

topText = Label(tab2, text="Edit your file path!", font=("Arial", 16))
topText.grid(row=0, column=0, columnspan=2, pady=10, sticky='n')

text5 = Label(tab2, text="Drive letter: ", font=("Arial", 12))
text5.grid(row=1, column=0, padx=5, pady=5, sticky='e')

comboBox = ttk.Combobox(tab2, state="readonly", values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
comboBox.grid(row=1, column=1, padx=5, pady=5, sticky='w')

saveButton = tk.Button(tab2, text="   Save   ", bg="blue", font=("sans-serif", 11), fg="white", command=wrap_save_settings)
saveButton.grid(row=2,column=0, columnspan=2, pady=10, sticky='n')

# Adding a canvas to display messages
canvas = tk.Canvas(tab1,height=300,width=900)
canvas.pack(padx=20, pady=20)

# Keyboard function when pressed "Enter" it will activate functions
keyboard.add_hotkey('enter',lambda:(wrap_move_files(),wrap_save_settings()))

root.mainloop()