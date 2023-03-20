#!/bin/python3
"""
Main function to construct and build the projects
"""
import os

from tkinter import Tk

import  magpype.manager as mpmanager
import magpype.magpype_gui as mpgui

def main():
    """Set up drives and for project"""
    options = [
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

    id_codes = {
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

    window = Tk()
    manager = mpmanager.PathManager(project_drive, options, id_codes)
    manager.set_broadcast_dir(broadcast_dir)
    manager.set_digital_dir(digital_dir)
    manager.set_print_dir(print_dir)
    gui = mpgui.Magpype_GUI(window, manager)
    window.mainloop()