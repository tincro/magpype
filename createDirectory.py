# !/usr/bin/python3

import os
import re
import subprocess
from distutils.dir_util import copy_tree
from shutil import copy2
from datetime import date
from tkinter import *

# Location of where to put the Directory
home = os.getcwd()
desktop = home + '\\Desktop\\' # Will output to Desktop

# What month is it? Return as padded decimal Number
d = date.today()
curMonth = d.strftime('%m')
curYear = d.strftime('%y')
# Drop down options for the Franchise information
OPTIONS = [
"RSF", # FORD
"RSFU", # FORD USED
"RS2F", # FORD COMBO
"RSHF", # HOOSIER FORD
"RSC", # CHEVROLET
"RS3H", # HYUNDAI COMBO
"RSWH", # HYUNDAI WEST
"RSHA", # HYUNDAI AVON
"RS3K", # KIA COMBO
"RSK", # KIA SOUTH
"RSWK", # KIA WEST
"RSSK", # KIA SHADELAND
"RS3M", # MITSUBISHI COMBO
"RSM", # MITSUBISHI SOUTH
"RSWMI", # MITSUBISHI WEST
"RS2BG", # BUICK / GMC COMBO
"RSNEBG", # NORTHEAST BUICK GMC
"RS2MA", # MAZDA COMBO
"RSWMA", # MAZDA WEST
"RSNEMA", # MAZDA NORTHEAST
"RSAB", # ALL BRANDS
"RSBHPH", # BUY HERE PAY HERE
"RSFNW", # FIAT-NEW WHITELAND
"RSGEN" # GENESIS
]

# Dictionary to populate folders
BRANDS = {
    "RSF": "Ford", # FORD
    "RSFU": "Ford", # FORD USED
    "RS2F": "Ford", # FORD COMBO
    "RSHF": "Ford", # HOOSIER FORD
    "RSC": "Chevy", # CHEVROLET
    "RS3H": "Hyundai", # HYUNDAI COMBO
    "RSWH": "Hyundai", # HYUNDAI WEST
    "RSHA": "Hyundai", # HYUNDAI AVON
    "RS3K": "Kia", # KIA COMBO
    "RSK": "Kia", # KIA SOUTH
    "RSWK": "Kia", # KIA WEST
    "RSSK": "Kia", # KIA SHADELAND
    "RS3M": "Mitsubishi", # MITSUBISHI COMBO
    "RSM": "Mitsubishi", # MITSUBISHI SOUTH
    "RSWMI": "Mitsubishi", # MITSUBISHI WEST
    "RS2BG": "Buick_GMC", # BUICK / GMC COMBO
    "RSNEBG": "Buick_GMC", # NORTHEAST BUICK GMC
    "RS2MA": "Mazda", # MAZDA COMBO
    "RSWMA": "Mazda", # MAZDA WEST
    "RSNEMA": "Mazda", # MAZDA NORTHEAST
    "RSAB": "Ray_Skillman_All_Brands", # ALL BRANDS
    "RSBHPH": "Ray_Buy Here Pay Here", # BUY HERE PAY HERE
    "RSFNW": "New Whiteland", # FIAT-NEW WHITELAND
    "RSGEN": "Genesis" # Genesis
}

defaultDir = "R:\\Broadcast"
# Open the project directory location in Explorer
def openFileLoc(dirLocation=defaultDir):
    subprocess.Popen('explorer ' + dirLocation)
# Decides which brand the folder belongs to per Franchise name
def whichBrand(brandName):
    return BRANDS[brandName]
#  Activate the dropdown per the radiobutton selected
def sel():
    if(mediaVar.get() == "Digital"):
        digi_Menu.config(state = ACTIVE)
    else:
        digi_Menu.config(state = DISABLED)
    if(mediaVar.get() == "Print"):
        print_Menu.config(state = ACTIVE)
    else:
        print_Menu.config(state = DISABLED)
# Change the Franchise Label text for readability
def franDescChange(*args):
    fn_DescText = "Folder: " + whichBrand(fn_TextVar.get())
    fn_Desc.config(text = fn_DescText)
# Build directory to the desired location per entry fields when button pressed
def createDir(*args):
    # Decide which type of Media the directory belongs to
    medName = mediaVar.get()
    if(medName == "Digital"): # isDigital
        parName = digi_Var.get()
    elif(medName == "Print"): # isPrint
        parName = print_Var.get()
    else:
        parName = whichBrand(fn_TextVar.get()) # isBroadcast (default)

    # Grab the directory parent Location
    toRen = "R:\\" + medName + "\\" + parName + "\\" # Change to where you want the folders to go
    # Grab the directory name
    franch_Name = fn_TextVar.get() # Franchise variable
    spot_Name = sn_NameEntry.get() # Spot name variable
    version_Name = vn_NameEntry.get() # version number
    month_Name = mn_NameEntry.get() # month number

    campaign_name = curYear + "-" + spot_Name # EX. _19-MyCampaignName_

    dirName = franch_Name + "_" + month_Name + "_" + campaign_name + "_" + "v" + version_Name

    # Path to copy
    aePath = 'S:\\Templates\\Files\\Ae'
    prePath = 'S:\\Templates\\Files\\Pre'
    # Files to copy
    aeFileTemp = 'Code_CampaignNumber_CampaignName_Version_001.aep'
    preFileTemp = 'Code_CampaignNumber_CampaignName_Version_001.prproj'

    aeFile = aePath + '\\' + aeFileTemp
    preFile = prePath + '\\' + preFileTemp

    # Create File Directory
    aeDir = toRen + dirName + '\\Files\\AE'
    preDir = toRen + dirName + '\\Files\\PR'
    gsDir = toRen + dirName + '\\GS'
    imgDir = toRen + dirName + '\\Images'
    audioDir = toRen + dirName + '\\Audio'
    radioDir = toRen + dirName + '\\Radio'
    bRollDir = toRen + dirName + '\\Broll'
    talentDir = toRen + dirName + '\\Talent'
    scriptDir = toRen + dirName + '\\Scripts'
    renDir = toRen + dirName + '\\Renders\\LOWRES'

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
    # Open the file location in Explorer
    openFileLoc(toRen + dirName)

# Create UI Window
mainWin = Tk()
mainWin.title("Create New Directory")
mainWin.geometry("490x265") # Size dimensions of floating window (W x H)

# Labels for Entry fields
sn_LabelText = "Spot Title:"
fn_LabelText = "Franchise Name:"
vn_LabelText = "Version:"
mn_LabelText = "Month:"

# Store string variables here
sn_TextVar = StringVar() # Spot Name
fn_TextVar = StringVar() # Franchise Name
vn_TextVar = StringVar() # Version Number
mn_TextVar = StringVar() # Month Number

# Default values for String variables
vn_TextVar.set("001") # Version default : 001
mn_TextVar.set(curMonth) # Month default: Today's Month Number
fn_TextVar.set(OPTIONS[1]) # Franchise default: RS2F
sn_TextVar.set("NewSpotNameHere") # Spot name default: "NewSpotNameHere"
# Padding for the entry fields widgets
padding_Y = 3
padding_X = 15

# Create Franchise Name Entry
fn_EntryLabel = Label(mainWin, text = fn_LabelText).grid(row = 0, column = 0, pady = padding_Y)
fn_NameEntry = OptionMenu(mainWin, fn_TextVar, *OPTIONS, command = franDescChange)
fn_NameEntry.grid(row = 0, column = 1, pady = padding_Y)
fn_Desc = Label(mainWin)
fn_Desc.grid(row = 0, column = 2, pady = padding_Y, columnspan=2, sticky=(W))
# Create Spot Name Entry
sn_EntryLabel = Label(mainWin, text = sn_LabelText).grid(row = 1, column = 0, pady = padding_Y)
sn_NameEntry = Entry(mainWin, textvariable = sn_TextVar, bd=5)
sn_NameEntry.grid(row = 1, column = 1, pady = padding_Y)
# Create Month Number Entry
mn_EntryLabel = Label(mainWin, text = mn_LabelText).grid(row = 2, column = 0, pady = padding_Y)
mn_NameEntry = Entry(mainWin, textvariable = mn_TextVar, bd=5)
mn_NameEntry.grid(row = 2, column = 1, pady = padding_Y)
# Create Version Number Entry
vn_EntryLabel = Label(mainWin, text = vn_LabelText).grid(row = 3, column = 0, pady = padding_Y)
vn_NameEntry = Entry(mainWin, textvariable = vn_TextVar, bd=5)
vn_NameEntry.grid(row = 3, column = 1, pady = padding_Y)

# What is this media intended for?  Broadcast, Digital, Print
medLabel = Label(mainWin, text="Create project for: ").grid(row = 4, column = 0, pady = padding_Y)
mediaVar = StringVar() # Variable to store the value
med_val1 = Radiobutton(mainWin, text = "Broadcast", variable = mediaVar, value = "Broadcast", command = sel)
med_val1.grid(row=4, column=1, sticky = (W))
med_val2 = Radiobutton(mainWin, text = "Digital", variable = mediaVar, value = "Digital", command = sel)
med_val2.grid(row=5, column=1, sticky=(W))
med_val3 = Radiobutton(mainWin, text = "Print", variable = mediaVar, value = "Print", command = sel)
med_val3.grid(row=6, column=1, sticky=(W))

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
digi_Var = StringVar() # Variable to store the dropdown value
digi_Menu = OptionMenu(mainWin, digi_Var, *digi_options)
digi_Menu.grid(row = 5, column = 2, columnspan=2, sticky=(W))
# Create drop down menu for the Print parent folder
print_Var = StringVar() # Variable to store the dropdown value
print_Menu = OptionMenu(mainWin, print_Var, *print_options)
print_Menu.grid(row = 6, column = 2, columnspan=2, sticky=(W))

# Set default button pressed for mediaVar and disable the drop downs
med_val1.select()
digi_Menu.config(state = DISABLED)
print_Menu.config(state = DISABLED)
# Set default folder name defaults
franDescChange()
fn_Desc.config(bg = '#C0392B', fg = '#FFFFFF')

# Create Directory Button
createBtn = Button(mainWin, text = "Create Directory", command = createDir)
createBtn.config(bg = '#3498DB', fg = '#FFFFFF') # change colors to blue with white text
createBtn.grid(row = 7, column = 0, padx = padding_X) # place on the bottom of the window

# Open Broadcast Directory Location
dirBtn = Button(mainWin, text = "Open Projects", command = openFileLoc)
dirBtn.config(bg='#A393B3', fg = '#FFFFFF')
dirBtn.grid(row = 6, column = 0, padx = padding_X)

mainWin.mainloop()
