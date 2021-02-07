#!/usr/bin/python3
"""
This module is used to manage some functionality for the AC_Magpype_GUI,
handling certain data found on the system. It's main responsibility is to construct the
drives that the GUI points to, and to hold the information that is on the drive.
"""
import os
from shutil import copy2
from datetime import date

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
    def __init__(self, project_drive, options, id_code_dict):
        self.project_drive = project_drive
        self.options = options
        self.id_code = id_code_dict

        self.broadcast_dir = None
        self.digital_dir = None
        self.print_dir = None

        self.default_drive = self.project_drive
        self.default_dir = self.broadcast_dir

    def brandname(self, brand_name):
        """Find which brand in the dictionary and return the proper label."""
        return self.id_code[brand_name]

    def set_broadcast_dir(self, broadcast_dir):
        """Set the broadcast directory location on the drive."""
        self.broadcast_dir = broadcast_dir

    def set_digital_dir(self, digital_dir):
        """Set the digital directory location on the drive."""
        self.digital_dir = digital_dir

    def set_print_dir(self, print_dir):
        """Set the print directory location on the drive."""
        self.print_dir = print_dir

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

class AC_Template:
    """Magement class to control templates."""
    def __init__(self, template_name, extension, parent_dir, destination):
        self.template_name = template_name
        self.extension = extension
        self.parent_dir = parent_dir
        self.destination = destination
        self.template_drive = None

    def set_template_drive(self, template_drive):
        """Set template drive. Use before copying any templates as it will break otherwise."""
        self.template_drive = template_drive

    def copy_template(self, new_file_name, rename=True):
        """Copy the template file into the new directory with correct naming."""
        file_path = os.path.join(self.template_drive, self.parent_dir)
        file_short_name = "{0}.{1}".format(self.template_name, self.extension)
        file_long_name = os.path.join(file_path, file_short_name)
        file_destination = os.path.join(self.destination, self.parent_dir)

        if os.path.exists(file_long_name):
            file_copy = copy2(file_long_name, file_destination)

            if rename:
                file_rename = "{0}.{1}".format(os.path.join(file_destination, new_file_name), self.extension)
                self.rename_template(file_copy, file_rename)

    def rename_template(self, file, destination):
        """Rename template to new project name convention"""
        os.rename(file, destination)
