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
curMonth = d.strftime('%m')
curYear = d.strftime('%y')
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

defaultDir = "R:\\Broadcast"
defaultDrive = "R:"
# Open the project directory location in Explorer
def openFileLoc(*args):
    """Open the file location on the disk."""
    if len(args) > 1:
        subprocess.Popen('explorer {}\\{}\\{}'.format(defaultDrive, args[0], args[1]))
    else:
        subprocess.Popen('explorer {}'.format(defaultDir))

# Decides which brand the folder belongs to per Franchise name
def whichBrand(brandName):
    """Find which brand in the dictionary and return the proper label."""
    return BRANDS[brandName]

#  Activate the dropdown per the radiobutton selected
def sel():
    """Select which medium this project is for."""
    if(mediaVar.get() == "Digital"):
        digi_Menu.config(state = ACTIVE, bg='#3498DB', fg='#FFFFFF')
    else:
        digi_Menu.config(state = DISABLED, bg="#999999")
    if(mediaVar.get() == "Print"):
        print_Menu.config(state = ACTIVE, bg='#3498DB', fg='#FFFFFF')
    else:
        print_Menu.config(state = DISABLED, bg="#999999")

# Change the Franchise Label text for readability
def franDescChange(*args):
    """Callback for changing the Franchise name options to the destination folder."""
    fn_Desc.delete(0, END)
    for item in whichBrand(fn_TextVar.get()):
        fn_Desc.insert(END, item)
    fn_Desc.activate(0)

# Build directory to the desired location per entry fields when button pressed
def createDir(*args):
    """Create a directory with the given parameters as the name of the directory.
    Copies and renames a template project for media files with same name."""
    # Decide which type of Media the directory belongs to
    medName = mediaVar.get()
    if(medName == "Digital"):
        # if media is Digital
        parName = digi_Var.get()
    elif(medName == "Print"):
        # if media is Print
        parName = print_Var.get()
    else:
        #  Get franchise name. Broadcast is default
        parName = fn_TextVar.get()

    # Grab the directory parent Location  EX. ..\Broadcast\Ford\
    toRen = "R:\\{}\\{}".format(medName, parName)
    # Grab the ISCI code for the spot
    franch_Name = fn_Desc.get(ACTIVE)
    # Television Spot name variable from user input
    spot_Name = processLabel(sn_NameEntry.get())
    # version number from user input
    version_Name = vn_NameEntry.get()
    # get month number from user input
    month_Name = mn_NameEntry.get()

    # EX. .._19-MyCampaignName_..
    campaign_name = curYear + "-" + spot_Name

    # directory name EX: RS2F_12_TruckMonth_v001
    dirName = franch_Name + "_" + month_Name + "_" + campaign_name + "_" + "v" + version_Name

    # Path to copy
    aePath = os.path.join('S:','Templates','Files','Ae')
    prePath = os.path.join('S:','Templates','Files','Pre')
    # Files to copy
    aeFileTemp = 'Code_CampaignNumber_CampaignName_Version_001.aep'
    preFileTemp = 'Code_CampaignNumber_CampaignName_Version_001.prproj'

    aeFile = os.path.join(aePath,aeFileTemp)
    preFile = os.path.join(prePath, preFileTemp)

    # Structure of project directory folders
    aeDir = os.path.join(toRen, dirName, 'Files', 'AE')
    preDir = os.path.join(toRen, dirName, 'Files', 'PR')
    gsDir = os.path.join(toRen, dirName,'GS')
    imgDir = os.path.join(toRen, dirName, 'Images')
    audioDir = os.path.join(toRen, dirName, 'Audio')
    radioDir = os.path.join(toRen, dirName, 'Radio')
    bRollDir = os.path.join(toRen,dirName,'Broll')
    talentDir = os.path.join(toRen, dirName, 'Talent')
    scriptDir = os.path.join(toRen, dirName, 'Scripts')
    renDir = os.path.join(toRen,dirName,'Renders', 'LOWRES')
    # Create the directory
    os.makedirs(aeDir)
    os.makedirs(preDir)
    os.makedirs(gsDir)
    os.makedirs(imgDir)
    os.makedirs(audioDir)
    os.makedirs(radioDir)
    os.makedirs(bRollDir)
    os.makedirs(talentDir)
    os.makedirs(scriptDir)
    os.makedirs(renDir)

    # Copy AE and PR file templates, rename to dirName
    aeCopyFile = copy2(aeFile, aeDir)
    preCopyFile = copy2(preFile, preDir)
    os.rename(aeCopyFile, aeDir + '\\' + dirName + '.aep')
    os.rename(preCopyFile, preDir + '\\' + dirName + '.prproj')
    # Open the file location in Explorer for convenience and confirmation
    openFileLoc("{}\\{}".format(medName, parName), dirName)

def processLabel(label_name):
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
        "Print": print_Var.get(),
        "Digital": digi_Var.get(),
        "Broadcast": fn_TextVar.get()
    }
    return media_dict.get(media, "Invalid media type")

def close_win():
    """Destroy the window."""
    mainWin.destroy()

# Window height and width
mainWin_w = 575
mainWin_h = 295
# Create UI Window
mainWin = Tk()
mainWin.title("Create New Directory")
mainWin.geometry("{}x{}".format((mainWin_w + 15), mainWin_h))

# Labels for Entry fields
sn_LabelText = "Spot Title:"
fn_LabelText = "Franchise Name:"
vn_LabelText = "Version:"
mn_LabelText = "Month:"

# Store string variables here
# Spot Name
sn_TextVar = StringVar(mainWin)
# Franchise Name
fn_TextVar = StringVar(mainWin)
# Version Number
vn_TextVar = StringVar(mainWin)
# Month Number
mn_TextVar = StringVar(mainWin)

# Default values for String variables
# Version default : 001
vn_TextVar.set("001")
# Month default: Today's Month Number
mn_TextVar.set(curMonth)
# Franchise default: RS2F
fn_TextVar.set(OPTIONS[0])
# Spot name default: "NewSpotNameHere"
sn_TextVar.set("NewSpotNameHere")

# Padding for the entry fields widgets and buttons
padding_Y = 3
padding_X = 15
btn_pady = 10

# Font styling
font_size = 12
font_family = 'Oswald'
font_weight = 'bold'

# Find Franchise Brand Name
fn_BrandLabel = Label(mainWin, text=fn_LabelText,
                     font=(font_family, font_size, font_weight)).grid(row=0, column=0, pady=padding_Y, sticky="e")
fn_NameEntry = OptionMenu(mainWin, fn_TextVar, *OPTIONS, command=franDescChange)
fn_NameEntry.grid(row=0, column=1, pady=padding_Y, sticky="w")
fn_NameEntry.config(bg='#3498DB', fg='#FFFFFF',
                    activebackground='#6DB9EC', activeforeground='#5C5C5C', width=25)

# Franchise name destination label with ISCI code
fn_Desc = Listbox(mainWin)
fn_Desc.grid(row = 0, column=2, pady=padding_Y, rowspan=2, columnspan=2, sticky="w")
# resize Franchise name label to the 4 - size to keep consistency
fn_size_dif = (4 - fn_Desc.size())
fn_Desc.config(height=fn_Desc.size() + fn_size_dif, )
franDescChange()

# Create Spot Name Entry
sn_EntryLabel = Label(mainWin, text=sn_LabelText,
                     font=(font_family, font_size, font_weight)).grid(row=1, column=0, pady=padding_Y, sticky="e")
sn_NameEntry = Entry(mainWin, textvariable=sn_TextVar, bd=5)
sn_NameEntry.grid(row=1, column=1, pady=padding_Y, padx=5, sticky="w")
# Create Month Number Entry
mn_EntryLabel = Label(mainWin, text=mn_LabelText,
                     font=(font_family, font_size, font_weight)).grid(row=2, column=0, pady=padding_Y, sticky="e")
mn_NameEntry = Entry(mainWin, textvariable=mn_TextVar, bd=5)
mn_NameEntry.grid(row=2, column=1, pady=padding_Y, padx=5, sticky="w")
# Create Version Number Entry
vn_EntryLabel = Label(mainWin, text=vn_LabelText,
                     font=(font_family, font_size, font_weight)).grid(row=3, column=0, pady=padding_Y, sticky="e")
vn_NameEntry = Entry(mainWin, textvariable=vn_TextVar, bd=5)
vn_NameEntry.grid(row=3, column=1, pady=padding_Y, padx=5, sticky="w")

# What is this media intended for?  Broadcast, Digital, Print
medLabel = Label(mainWin, text="Create project for: ",
                font=(font_family, font_size, font_weight)).grid(row=4, column=0, pady=padding_Y, sticky="e")
# Variable to store the value
mediaVar = StringVar(mainWin)
# Create Radio buttons for the media types available
med_val1 = Radiobutton(mainWin, text="Broadcast", variable=mediaVar, value="Broadcast", command=sel)
med_val1.grid(row=4, column=1, sticky="w")
med_val2 = Radiobutton(mainWin, text="Digital", variable=mediaVar, value="Digital", command=sel)
med_val2.grid(row=5, column=1, sticky="w")
med_val3 = Radiobutton(mainWin, text="Print", variable=mediaVar, value="Print", command=sel)
med_val3.grid(row=6, column=1, sticky="w")

# Dynamically populate the Digital dropdown list
digi_folder = "R:\\Digital\\"
digi_options = []
digi_optionsToAppend = os.listdir(digi_folder)
for digiItem in digi_optionsToAppend:
    if(digiItem[0] == '.'):
        continue
    else:
        digi_options.append(digiItem)

# Dynamically populate the Print dropdown list
print_folder = "R:\\Print\\"
print_options = []
print_optionsToAppend = os.listdir(print_folder)
for printItem in print_optionsToAppend:
    if(printItem[0] == '.'): # Skip if hidden folder
        continue
    else:
        print_options.append(printItem)

# Create drop down menu for the Digital parent folder
# Variable to store the dropdown value
digi_Var = StringVar(mainWin)
digi_Menu = OptionMenu(mainWin, digi_Var, *digi_options)
digi_Menu.grid(row=5, column=1, columnspan=2, sticky="w", padx=padding_X*6)
digi_Menu.config(width=35, background="#999999",
                activebackground='#6DB9EC', activeforeground='#5C5C5C')
# Create drop down menu for the Print parent folder
# Variable to store the dropdown value
print_Var = StringVar(mainWin)
print_Menu = OptionMenu(mainWin, print_Var, *print_options)
print_Menu.grid(row=6, column=1, columnspan=2, sticky="w", padx=padding_X*6)
print_Menu.config(width=35, background="#999999",
                    activebackground='#6DB9EC', activeforeground='#5C5C5C')

# Set default button pressed for mediaVar and disable the drop downs
med_val1.select()
digi_Menu.config(state=DISABLED)
print_Menu.config(state=DISABLED)

# Add separator for organization
sep = ttk.Separator(mainWin, orient="horizontal")
sep.grid(row=7, column=0, columnspan=4, padx=padding_X, pady=btn_pady, sticky="we")

# Open Projects Directory Location button
dirBtn = Button(mainWin, text="Open Projects",
                command=lambda: openFileLoc(mediaVar.get(), get_media(mediaVar.get())))
dirBtn.config(bg='#A393B3', fg='#FFFFFF', width=16,
                activebackground='#B8A7CA', activeforeground='#5C5C5C')
dirBtn.grid(row=8, column=0, padx=padding_X, sticky="e")

# Create Directory Button
createBtn = Button(mainWin, text="Create Directory", command=createDir)
createBtn.config(bg='#3498DB', fg='#FFFFFF', width=16,
                activebackground='#6DB9EC', activeforeground='#5C5C5C') # change colors to blue with white text
createBtn.grid(row=8, column=1, sticky="w") # place on the bottom of the window

# Close Window Button
closeBtn = Button(mainWin, text="Close", command=close_win)
closeBtn.config(bg='#C0392B', fg='#FFFFFF', width=16,
                activebackground='#E55647', activeforeground='#5C5C5C') # change colors to red with white text
closeBtn.grid(row=8, column=2, padx=padding_X, sticky="e") # place on the bottom of the window

mainWin.mainloop()
