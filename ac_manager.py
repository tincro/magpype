#!/usr/bin/python3

import os
import subprocess
from shutil import copy2
from datetime import date

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

project_drive = "R:"
broadcast_dir = os.path.join(project_drive,"Broadcast")
digital_dir = os.path.join(project_drive, "Digital")
print_dir = os.path.join(project_drive, "Print")

# digital_dir = acm.digital_dir
# digital_list = []
# digital_pop = os.listdir(digital_dir)
# populate(digital_pop, digital_list)

class AC_ProjectList:
    """List of projects in a directory."""
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.list = []
        self.pop = os.listdir(dir_name)
        self.populate(self.pop, self.list)

    def populate(self, source, destination):
        """Dynamically populate the dropdownlist with existing folders"""
        for item in source:
            if(item.startswith(".")):
                continue
            else:
                destination.append(item)
        return destination

class AC_PathManager:
    """Management class for path building."""
    def __init__(self, project_drive=project_drive, broadcast_dir=broadcast_dir,
                digital_dir=digital_dir, print_dir=print_dir, options=OPTIONS,
                id_code_dict=BRANDS):
        self.project_drive = project_drive
        self.broadcast_dir = broadcast_dir
        self.digital_dir = digital_dir
        self.print_dir = print_dir
        self.options = options
        self.id_code = id_code_dict

        self.default_drive = self.project_drive
        self.default_dir = self.broadcast_dir

    def brandname(self, brandName):
        """Find which brand in the dictionary and return the proper label."""
        return self.id_code[brandName]

    def copy_template(self, path_to_file, destination, new_file_name,
                    file_extension, rename=True):
        """Copy the template file into the new directory with correct naming."""
        file_name = "{0}.{1}".format(path_to_file, file_extension)
        file_copy = copy2(file_name, destination)
        file_rename = "{0}.{1}".format(
                    os.path.join(destination, new_file_name), file_extension)
        if rename:
            self.rename_template(file_copy, file_rename)

    def make_folders(self, render_directory, directory_name, folders):
        """Make folders for the directory given the list of folders build."""
        for folder in folders:
            dir = os.path.join(render_directory, directory_name, folder)
            os.makedirs(dir)

    def openpath(self,*args):
        """Callback to open the file location on the disk."""
        if len(args) > 1:
            subprocess.Popen('explorer {}\\{}\\{}'.format(self.project_drive, args[0], args[1]))
        else:
            subprocess.Popen('explorer {}'.format(self.default_dir))

    def process_label(self, label_name):
        """Process the label name for consistency.
        Removes all whitespace and capitalizes each word."""
        if " " in label_name:
            split_arr = label_name.split(" ")
            capitalized = [x.capitalize() for x in split_arr]
            processed = "".join(capitalized).replace(" ", "")
        else:
            processed = label_name
        return processed

    def rename_template(self, file, destination):
        os.rename(file, destination)


class AC_DateManager:
    """Management class to hold constant information."""
    month_name = {
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

    def __init__(self):
        self.today = date.today()
        self.current_month = self.today.strftime('%m')
        self.current_year = self.today.strftime('%y')

    def get_month(self, month):
        """Get the calendar month to string."""
        month_num = int(month)
        return AC_DateManager.month_name[month_num]
