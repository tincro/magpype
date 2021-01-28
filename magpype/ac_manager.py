#!/usr/bin/python3
"""
This module is used to manage some functionality for the magpie_gui,
handling certain data found on the system. It's main responsibility is to construct the
drives that the GUI points to, and to hold the information that is on the drive.

"""
import os
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

PROJECT_DRIVE = "R:"
BROADCAST_DIR = os.path.join(PROJECT_DRIVE,"Broadcast")
DIGITAL_DIR = os.path.join(PROJECT_DRIVE, "Digital")
PRINT_DIR = os.path.join(PROJECT_DRIVE, "Print")

TEMPLATE_DRIVE = "S:"
TEMPLATE_DIR = os.path.join(TEMPLATE_DRIVE, "Templates")

class AC_ProjectList:
    """List of projects in a directory."""
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.list = []
        self.pop = os.listdir(self.dir_name)
        self.populate(self.pop, self.list)

    def populate(self, source, destination):
        """Dynamically populate the dropdownlist with existing folders"""
        for item in source:
            if item.startswith("."):
                continue
            destination.append(item)
        return destination

class AC_PathManager:
    """Management class for path building."""
    def __init__(self, project_drive=PROJECT_DRIVE, broadcast_dir=BROADCAST_DIR,
                digital_dir=DIGITAL_DIR, print_dir=PRINT_DIR,                
                options=OPTIONS, id_code_dict=BRANDS):
        self.project_drive = project_drive
        self.broadcast_dir = broadcast_dir
        self.digital_dir = digital_dir
        self.print_dir = print_dir

        self.options = options
        self.id_code = id_code_dict

        self.default_drive = self.project_drive
        self.default_dir = self.broadcast_dir

    def brandname(self, brand_name):
        """Find which brand in the dictionary and return the proper label."""
        return self.id_code[brand_name]

    # def copy_template(self, path_to_file, destination, new_file_name,
    #                 file_extension, rename=True):
    #     """Copy the template file into the new directory with correct naming."""
    #     file_name = "{0}.{1}".format(path_to_file, file_extension)
    #     file_copy = copy2(file_name, destination)
    #     file_rename = "{0}.{1}".format(
    #                 os.path.join(destination, new_file_name), file_extension)
    #     if rename:
    #         self.rename_template(file_copy, file_rename)

    def make_folders(self, render_directory, directory_name, folders):
        """Make folders for the directory given the list of folders build."""
        for folder in folders:
            directory = os.path.join(render_directory, directory_name, folder)
            os.makedirs(directory)

    def process_label(self, label_name):
        """Process the label name for consistency.
        Removes all whitespace and capitalizes each word. Will not process if no
        whitespace exists."""
        if " " in label_name:
            split_arr = label_name.split(" ")
            capitalized = [x.capitalize() for x in split_arr]
            processed = "".join(capitalized).replace(" ", "")
        else:
            processed = label_name
        return processed

    # def rename_template(self, file, destination):
    #     os.rename(file, destination)


class AC_DateManager:
    """Management class to hold constant information."""

    def __init__(self):
        self.today = date.today()
        self.current_month = self.today.strftime('%m')
        self.current_year = self.today.strftime('%y')
        self.month_name = {
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

    def get_month(self, month):
        """Get the calendar month to string."""
        month_num = int(month)
        return self.month_name[month_num]

class AC_Template:
    """Magement class to control templates."""
    def __init__(self, template_name, extension, parent_dir, destination):
        self.template_name = template_name
        self.extension = extension
        self.parent_dir = parent_dir
        self.destination = destination
        
        self.template_drive = TEMPLATE_DIR        

    def copy_template(self, new_file_name, rename=True):
        """Copy the template file into the new directory with correct naming."""
        file_path = os.path.join(self.template_drive, self.parent_dir)
        file_name = os.path.join(file_path, self.template_name, self.extension)
        file_destination = os.path.join(self.destination, self.parent_dir)
        
        file_copy = copy2(file_name, file_destination)
        
        if rename:
            file_rename = "{0}.{1}".format(os.path.join(file_destination, new_file_name), self.extension)
            self.rename_template(file_copy, file_rename)

        # ae_path = os.path.join(template_path, ae_dir)
        # ae_file = os.path.join(ae_path, temp_file_name)
        # ae_dest = os.path.join(render_dir, dir_name, ae_dir)
        # self.manager.copy_template(ae_file, ae_dest, dir_name, 'aep')

        # ae_template = AC_Template(template_name, 'Files//AE', 'aep')

    def rename_template(self, file, destination):
        """Rename template to new project name convention"""
        os.rename(file, destination)