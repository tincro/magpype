# !/usr/bin/python3

import os
import re
import subprocess
from distutils.dir_util import copy_tree
from shutil import copy2
from datetime import date
from tkinter import *
from tkinter import ttk

# Location of where to put the Directory
home = os.getcwd()
desktop = os.path.join(home,"Desktop","")

# What month is it? Return as padded decimal Number
d = date.today()
current_month = d.strftime('%m')
current_year = d.strftime('%y')

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

default_dir = "R:\\Broadcast"
default_drive = "R:"
# Open the project directory location in Explorer
def openpath(*args):
    """Open the file location on the disk."""
    if len(args) > 1:
        # file_path = os.path.join(default_drive, args[0], args[1])
        # print(file_path)
        subprocess.Popen('explorer {}\\{}\\{}'.format(default_drive, args[0], args[1]))
    else:
        subprocess.Popen('explorer {}'.format(default_dir))

# Decides which brand the folder belongs to per Franchise name
def brandname(brandName):
    """Find which brand in the dictionary and return the proper label."""
    return BRANDS[brandName]

#  Activate the dropdown per the radiobutton selected
def sel():
    """Select which medium this project is for."""
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

# Build directory to the desired location per entry fields when button pressed
def create_dir(*args):
    """Create a directory with the given parameters as the name of the directory.
    Copies and renames a template project for media files with same name."""
    # Decide which type of Media the directory belongs to
    media = media_var.get()
    if(media == "Digital"):
        # if media is Digital
        parent_dir = digital_var.get()
    elif(media == "Print"):
        # if media is Print
        parent_dir = print_var.get()
    else:
        #  Get franchise name. Broadcast is default
        parent_dir = brand_var.get()

    # Grab the directory parent Location  EX. ..\Broadcast\Ford\
    render_dir = "R:\\{}\\{}".format(media, parent_dir)
    # Grab the ISCI code for the spot
    brand_name = destination.get(ACTIVE)
    # Television Spot name variable from user input
    spot_name = process_label(spot_entry.get())
    # version number from user input
    version_name = version_entry.get()
    # get month number from user input
    month_name = month_entry.get()

    # EX. .._19-MyCampaignName_..
    campaign_name = current_year + "-" + spot_name

    join_dirs = (brand_name, month_name, campaign_name, version_name.zfill(3))
    # directory name EX: RS2F_12_TruckMonth_v001
    dir_name = "_".join(join_dirs)

    # Path to copy
    ae_path  = os.path.join('S:','Templates','Files','Ae')
    pre_path = os.path.join('S:','Templates','Files','Pre')
    # Files to copy
    ae_temp = 'Code_CampaignNumber_CampaignName_Version_001.aep'
    pre_temp = 'Code_CampaignNumber_CampaignName_Version_001.prproj'

    ae_file  = os.path.join(ae_path,ae_temp)
    pre_file = os.path.join(pre_path, pre_temp)

    # Structure of project directory folders
    ae_dir     = os.path.join(render_dir, dir_name, 'Files', 'AE')
    pre_dir    = os.path.join(render_dir, dir_name, 'Files', 'PR')
    gs_dir     = os.path.join(render_dir, dir_name,'GS')
    img_dir    = os.path.join(render_dir, dir_name, 'Images')
    audio_dir  = os.path.join(render_dir, dir_name, 'Audio')
    radio_dir  = os.path.join(render_dir, dir_name, 'Radio')
    broll_dir  = os.path.join(render_dir,dir_name,'Broll')
    talent_dir = os.path.join(render_dir, dir_name, 'Talent')
    script_dir = os.path.join(render_dir, dir_name, 'Scripts')
    render_dir    = os.path.join(render_dir, dir_name,'Renders', 'LOWRES')
    # Create the directory
    os.makedirs(ae_dir)
    os.makedirs(pre_dir)
    os.makedirs(gs_dir)
    os.makedirs(img_dir)
    os.makedirs(audio_dir)
    os.makedirs(radio_dir)
    os.makedirs(broll_dir)
    os.makedirs(talent_dir)
    os.makedirs(script_dir)
    os.makedirs(render_dir)

    # Copy AE and PR file templates, rename to dir_name
    ae_copy = copy2(ae_file, ae_dir)
    pre_copy = copy2(pre_file, pre_dir)
    os.rename(ae_copy, ae_dir + '\\' + dir_name + '.aep')
    os.rename(pre_copy, pre_dir + '\\' + dir_name + '.prproj')
    # Open the file location in Explorer for convenience and confirmation
    openpath("{}\\{}".format(media, parent_dir), dir_name)

def process_label(label_name):
    """
    Process the label name for consistency.
    Removes all whitespace and capitalizes each word.
    """
    # Remove whitespace if there is any in the name
    if " " in label_name:
        split_arr = label_name.split(" ")
        capitalized = [x.capitalize() for x in split_arr]
        processed = "".join(capitalized).replace(" ", "")
    else:
        # if not, keep the same name
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
# Spot Name
spot_var = StringVar(window)
# Franchise Name
brand_var = StringVar(window)
# Version Number
version_var = StringVar(window)
# Month Number
month_var = StringVar(window)

# Default values for String variables
# Version default : 001
version_var.set("1")
# Month default: Today's Month Number
month_var.set(current_month)
# Franchise default: RS2F
brand_var.set(OPTIONS[0])
# Spot name default: "NewSpotNameHere"
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

# Variable to store the value
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
digital_dir = "R:\\Digital\\"
digital_list = []
digital_pop = os.listdir(digital_dir)
populate(digital_pop, digital_list)

# Dynamically populate the Print dropdown list
print_folder = "R:\\Print\\"
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
