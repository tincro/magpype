# !/usr/bin/python3

import os
import re
import subprocess
from distutils.dir_util import copy_tree
from shutil import copy2
from datetime import date
from tkinter import *
from tkinter import ttk

# Drop down options for the Franchise information
OPTIONS = [
"Ford",
"Chevy",
"Hyundai",
"Kia",
"Mitsubishi",
"Buick_GMC",
"Mazda",
"New Whiteland",
"Genesis",
"Westside Auto Mall",
"Ray_Buy Here Pay Here",
"Ray_Skillman_All_Brands",
"Tent_Sale"
]

# Dictionary to populate folders
BRANDS = {
    "Ford": ["RS2F", "RSHF", "RSF", "RSFU"],
    "Chevy": ["RSC"],
    "Hyundai": ["RS3H", "RSH", "RSWH", "RSHA"],
    "Kia": ["RS3K", "RSK", "RSWK", "RSSK"],
    "Mitsubishi": ["RS3M", "RSM", "RSWMI"],
    "Buick_GMC": ["RS2BG", "RSNEBG","RS2G","RS2B"],
    "Mazda": ["RS2MA", "RSWMA", "RSNEMA"],
    "New Whiteland": ["RSFNW", "RSKNW", "RSBNW", "RSMNW"],
    "Genesis": ["RSG"],
    "Westside Auto Mall": ["RSWAM", "RSWT"],
    "Ray_Buy Here Pay Here": ["RSBHPH"],
    "Ray_Skillman_All_Brands": ["RSAB", "RSBF"],
    "Tent_Sale": ["TS"]
}

DAYS = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUL",
    7: "JUN",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC"
}

d = date.today()
current_month = d.strftime('%m')
current_year = d.strftime('%y')

default_dir = "R:\\Broadcast"
default_drive = "R:"

def openpath(*args):
    """Open the file location on the disk."""
    if len(args) > 1:
        subprocess.Popen('explorer {}\\{}\\{}'.format(default_drive, args[0], args[1]))
    else:
        subprocess.Popen('explorer {}'.format(default_dir))

def get_month(month):
    """Get the calendar month to string."""
    month_num = int(month)
    return DAYS[month_num]

def brandname(brandName):
    """Find which brand in the dictionary and return the proper label."""
    return BRANDS[brandName]

def sel():
    """Callback to select which medium this project is for."""
    if(media_var.get() == "Digital"):
        digital_menu.config(state = ACTIVE, bg='#3498DB', fg='#FFFFFF')
    else:
        digital_menu.config(state = DISABLED, bg="#999999")
    if(media_var.get() == "Print"):
        print_menu.config(state = ACTIVE, bg='#3498DB', fg='#FFFFFF')
    else:
        print_menu.config(state = DISABLED, bg="#999999")

# Change the Franchise Label text for readability
def on_brand_change(*args):
    """Callback for changing the Franchise name options to the destination folder."""
    destination.delete(0, END)
    for item in brandname(brand_var.get()):
        destination.insert(END, item)
    destination.activate(0)

def make_folders(render_directory, directory_name, folders):
    """Make folders for the directory given the list of folders to make"""
    for folder in folders:
        dir = os.path.join(render_directory, directory_name, folder)
        os.makedirs(dir)

def copy_template(path_to_file, destination, new_file_name, file_extension):
    """Copy the template file into the new directory with correct naming."""
    file_name = "{0}.{1}".format(path_to_file, file_extension)
    file_copy = copy2(file_name, destination)
    file_rename = "{0}.{1}".format(
                os.path.join(destination, new_file_name), file_extension)
    os.rename(file_copy, file_rename)

# Build directory to the desired location per entry fields when button pressed
def create_dir(*args):
    """Create a directory with the given parameters as the name of the directory.
    Copies and renames a template project for media files with same name."""
    # Decide which type of Media the directory belongs to
    media = media_var.get()
    if(media == "Digital"):
        parent_dir = digital_var.get()
    elif(media == "Print"):
        parent_dir = print_var.get()
    else:
        parent_dir = brand_var.get()

    # Grab the directory parent Location  EX. ..\Broadcast\Ford\
    # Grabs the current name for each part of the dir to build the location
    render_dir = os.path.join("R:", media, parent_dir)
    brand_name = destination.get(ACTIVE)
    spot_name = process_label(spot_entry.get())
    version_name = version_entry.get()
    month_number = month_entry.get()
    month_name = get_month(month_number)
    unique_name = (current_year, spot_name)
    campaign_name = "-".join(unique_name)
    version_padding = 3

    join_dirs = (brand_name, month_number, month_name,
                campaign_name, version_name.zfill(version_padding))
    dir_name = "_".join(join_dirs)

    ae_dir = os.path.join('Files','AE')
    pr_dir = os.path.join('Files', 'PR')
    folder_list = [
        'Audio',
        'Broll',
        ae_dir,
        pr_dir,
        'Graphics',
        'Images',
        'Radio',
        os.path.join('Render','LOWRES')
    ]

    make_folders(render_dir, dir_name, folder_list)

    template_path = os.path.join('S:', 'Templates')
    temp_file_name = 'Code_CampaignNumber_CampaignName_Version_001'

    ae_path = os.path.join(template_path, ae_dir)
    ae_file = os.path.join(ae_path, temp_file_name)
    ae_dest = os.path.join(render_dir, dir_name, ae_dir)

    pr_path = os.path.join(template_path, pr_dir)
    pr_file = os.path.join(pr_path, temp_file_name)
    pr_dest = os.path.join(render_dir, dir_name, pr_dir)

    copy_template(ae_file, ae_dest, dir_name, 'aep')
    copy_template(pr_file, pr_dest, dir_name, 'prproj')
    # Open the file location in Explorer for convenience and confirmation
    openpath("{}\\{}".format(media, parent_dir), dir_name)

def process_label(label_name):
    """Process the label name for consistency.
    Removes all whitespace and capitalizes each word."""
    if " " in label_name:
        split_arr = label_name.split(" ")
        capitalized = [x.capitalize() for x in split_arr]
        processed = "".join(capitalized).replace(" ", "")
    else:
        processed = label_name
    return processed

def get_media(media):
    """Return the media variable value."""
    media_dict = {
        "Print": print_var.get(),
        "Digital": digital_var.get(),
        "Broadcast": brand_var.get()
    }
    return media_dict.get(media, "Invalid media type")

def populate(source, destination):
    """Dynamically populate the dropdownlist with existing folders"""
    for item in source:
        if(item.startswith(".")):
            continue
        else:
            destination.append(item)
    return destination

def close_win():
    """Destroy the window."""
    window.destroy()

# Window height and width
winx, winy = (575, 295)

# Create UI Window
window = Tk()
window.title("Create New Directory")
window.geometry("{}x{}".format((winx + 15), winy))

# Labels for Entry fields
spot_text = "Spot Title:"
brand_text = "Brand Name:"
version_text = "Version:"
month_text = "Month:"

# Store string variables here
spot_var = StringVar(window)
brand_var = StringVar(window)
version_var = StringVar(window)
month_var = StringVar(window)

# Default values for String variables
version_var.set("1")
month_var.set(current_month)
brand_var.set(OPTIONS[0])
spot_var.set("NewSpotNameHere")

# Padding for the entry fields widgets and buttons
pady = 3
padx = 15
btn_pady = 10

# Font styling
font_size = 12
font_family = 'Oswald'
font_weight = 'bold'

# Find Franchise Brand Name
brand_label = Label(
                window,
                text=brand_text,
                font=(font_family, font_size, font_weight)
            ).grid(row=0, column=0, pady=pady, sticky="e")

brand_menu = OptionMenu(window, brand_var, *OPTIONS, command=on_brand_change)
brand_menu.grid(row=0, column=1, pady=pady, sticky="w")
brand_menu.config(bg='#3498DB', fg='#FFFFFF',
                    activebackground='#6DB9EC',
                    activeforeground='#5C5C5C', width=25)

# Brand name destination label with ISCI code
destination = Listbox(window)
destination.grid(row = 0, column=2, pady=pady,
            rowspan=2, columnspan=2, sticky="w")
# resize Brand name label to the 4 - size to keep consistency
brand_size = (4 - destination.size())
destination.config(height=destination.size() + brand_size, )
on_brand_change()

# Create Spot Name Entry
spot_label = Label(
                    window,
                    text=spot_text,
                    font=(font_family, font_size, font_weight)
                ).grid(row=1, column=0, pady=pady, sticky="e")

spot_entry = Entry(window, textvariable=spot_var, bd=5)
spot_entry.grid(row=1, column=1, pady=pady, padx=5, sticky="w")

# Create Month Number Entry
month_label = Label(
                    window,
                    text=month_text,
                    font=(font_family, font_size, font_weight)
                ).grid(row=2, column=0, pady=pady, sticky="e")

month_entry = Entry(window, textvariable=month_var, bd=5)
month_entry.grid(row=2, column=1, pady=pady, padx=5, sticky="w")

# Create Version Number Entry
version_label = Label(
                        window,
                        text=version_text,
                        font=(font_family, font_size, font_weight)
                    ).grid(row=3, column=0, pady=pady, sticky="e")

version_entry = Entry(window, textvariable=version_var, bd=5)
version_entry.grid(row=3, column=1, pady=pady, padx=5, sticky="w")

# What is this media intended for?  Broadcast, Digital, Print
media_label = Label(
                    window,
                    text="Create project for: ",
                    font=(font_family, font_size, font_weight)
                ).grid(row=4, column=0, pady=pady, sticky="e")

media_var = StringVar(window)
# Create Radio buttons for the media types available
broadcast_btn = Radiobutton(
                window,
                text="Broadcast",
                variable=media_var,
                value="Broadcast",
                command=sel
            )
broadcast_btn.grid(row=4, column=1, sticky="w")

digital_btn = Radiobutton(
                window,
                text="Digital",
                variable=media_var,
                value="Digital",
                command=sel
            )
digital_btn.grid(row=5, column=1, sticky="w")

print_btn = Radiobutton(
                window,
                text="Print",
                variable=media_var,
                value="Print",
                command=sel
            )
print_btn.grid(row=6, column=1, sticky="w")

# Dynamically populate the Digital dropdown list
digital_dir = os.path.join("R:", "Digital")
digital_list = []
digital_pop = os.listdir(digital_dir)
populate(digital_pop, digital_list)

# Dynamically populate the Print dropdown list
print_folder = os.path.join("R:", "Print")
print_options = []
print_pop = os.listdir(print_folder)
populate(print_pop, print_options)

# Create drop down menu for the Digital parent folder
# Variable to store the dropdown value
digital_var = StringVar(window)
digital_menu = OptionMenu(window, digital_var, *digital_list)
digital_menu.grid(row=5, column=1, columnspan=2, sticky="w", padx=padx*6)
digital_menu.config(width=35, background="#999999",
                activebackground='#6DB9EC', activeforeground='#5C5C5C')
# Create drop down menu for the Print parent folder
# Variable to store the dropdown value
print_var = StringVar(window)
print_menu = OptionMenu(window, print_var, *print_options)
print_menu.grid(row=6, column=1, columnspan=2, sticky="w", padx=padx*6)
print_menu.config(width=35, background="#999999",
                    activebackground='#6DB9EC', activeforeground='#5C5C5C')

# Set default button pressed for media_var and disable the drop downs
broadcast_btn.select()
digital_menu.config(state=DISABLED)
print_menu.config(state=DISABLED)

# Add separator for organization
sep = ttk.Separator(window, orient="horizontal")
sep.grid(row=7, column=0, columnspan=4, padx=padx, pady=btn_pady, sticky="we")

# Open Projects Directory Location button
open_btn = Button(window, text="Open Projects",
                command=lambda: openpath(media_var.get(), get_media(media_var.get())))
open_btn.config(bg='#A393B3', fg='#FFFFFF', width=16,
                activebackground='#B8A7CA', activeforeground='#5C5C5C')
open_btn.grid(row=8, column=0, padx=padx, sticky="e")

# Create Directory Button
create_btn = Button(window, text="Create Directory", command=create_dir)
create_btn.config(bg='#3498DB', fg='#FFFFFF', width=16,
                activebackground='#6DB9EC', activeforeground='#5C5C5C') # change colors to blue with white text
create_btn.grid(row=8, column=1, sticky="w") # place on the bottom of the window

# Close Window Button
close_btn = Button(window, text="Close", command=close_win)
close_btn.config(bg='#C0392B', fg='#FFFFFF', width=16,
                activebackground='#E55647', activeforeground='#5C5C5C') # change colors to red with white text
close_btn.grid(row=8, column=2, padx=padx, sticky="e") # place on the bottom of the window

window.mainloop()
