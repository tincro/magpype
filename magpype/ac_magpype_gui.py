#!/usr/bin/python3
"""
This module is designed to build a floating window GUI's.
It was designed as a solution for a project framework in a small studio.
"""

import os
import subprocess
from tkinter import *
from tkinter import ttk

from ac_manager import *

class AC_Magpype_GUI:
    """Class for creating floating desktop window. Framework for organization of
    production. Managed by AC_Manager."""

    def __init__(self, window, manager):
        self.manager = manager
        self.date = AC_DateManager()

        # Window construction information
        self.window = window
        self.title = "Create New Project"
        self.winx = 575
        self.winy = 295
        self.padx = 15
        self.pady = 3
        self.btn_padx = 16
        self.btn_pady = 10
        self.option_w = 25
        self.entry_pad = 5
        self.entry_grid_padx = 5
        self.window.title(self.title)
        self.window.geometry("{0}x{1}".format((self.winx + self.padx), self.winy))

        # Styling
        self.font_size = 12
        self.font_family = 'Roboto'
        self.font_weight = 'bold'
        self.blue = '#3498DB'
        self.active_blue = '#6DB9EC'
        self.white = '#FFFFFF'
        self.grey = '#999999'
        self.disable_grey = '#5C5C5C'
        self.purple = '#A393B3'
        self.active_purple = '#B8A7CA'
        self.red = '#C0392B'
        self.active_red = '#E55647'

        # Build the UI information
        self.brand_label_text = "Brand Name:"
        self.brand_var = StringVar(self.window)
        self.brand_var.set(self.manager.options[0])

        self.brand_label = Label(
            self.window, text=self.brand_label_text,
            font=(self.font_family, self.font_size, self.font_weight)
        ).grid(row=0, column=0, pady=self.pady, sticky="e")

        self.brand_menu = OptionMenu(self.window, self.brand_var, *self.manager.options,
                                command=self.on_brand_change)
        self.brand_menu.grid(row=0, column=1, pady=self.pady, sticky="w")
        self.brand_menu.config(bg=self.blue, fg=self.white,
                            activebackground=self.active_blue,
                            activeforeground=self.disable_grey, width=self.option_w
        )

        # Brand name destination label with ISCI code
        self.destination = Listbox(self.window)
        self.destination.grid(row = 0, column=2, pady=self.pady,
        rowspan=2, columnspan=2, sticky="w")
        # resize Brand name label to the 4 - size to keep consistency for list
        brand_size = (4 - self.destination.size())
        self.destination.config(height=self.destination.size() + brand_size, )
        # Initialize the list population
        self.on_brand_change()

        self.spot_label_text = "Spot Title:"
        self.spot_var = StringVar(self.window)
        self.spot_var.set("NewSpotNameHere")
        self.spot_label = Label(
                            self.window,
                            text=self.spot_label_text,
                            font=(self.font_family, self.font_size, self.font_weight)
        ).grid(row=1, column=0, pady=self.pady, sticky="e")

        self.spot_entry = Entry(self.window, textvariable=self.spot_var, bd=self.entry_pad)
        self.spot_entry.grid(row=1, column=1, pady=self.pady, padx=5, sticky="w")

        self.month_label_text = "Month:"
        self.month_var = StringVar(self.window)
        self.month_var.set(self.date.current_month)
        self.month_label = Label(
                            self.window,
                            text=self.month_label_text,
                            font=(self.font_family, self.font_size, self.font_weight)
        ).grid(row=2, column=0, pady=self.pady, sticky="e")

        self.month_entry = Entry(self.window, textvariable=self.month_var, bd=self.entry_pad)
        self.month_entry.grid(row=2, column=1, pady=self.pady, padx=self.entry_grid_padx, sticky="w")

        self.version_label_text = "Version:"
        self.version_var = StringVar(self.window)
        self.version_var.set("1")
        self.version_label = Label(
                            self.window,
                            text=self.version_label_text,
                            font=(self.font_family, self.font_size, self.font_weight)
        ).grid(row=3, column=0, pady=self.pady, sticky="e")

        self.version_entry = Entry(self.window, textvariable=self.version_var, bd=self.entry_pad)
        self.version_entry.grid(row=3, column=1, pady=self.pady, padx=self.entry_grid_padx, sticky="w")

        self.media_label_text = "Create project for:"
        self.media_var = StringVar(self.window)
        self.media_btns = ("Broadcast", "Digital", "Print")
        # What is this media intended for?  Broadcast, Digital, Print
        self.media_label = Label(
                            self.window,
                            text=self.media_label_text,
                            font=(self.font_family, self.font_size, self.font_weight)
        ).grid(row=4, column=0, pady=self.pady, sticky="e")

        # Radio buttons to select Media choice
        self.broadcast_btn = Radiobutton(
                                self.window,
                                text=self.media_btns[0],
                                variable=self.media_var,
                                value=self.media_btns[0],
                                command=self.sel
        )
        self.broadcast_btn.grid(row=4, column=1, sticky="w")

        self.digital_btn = Radiobutton(
                                self.window,
                                text=self.media_btns[1],
                                variable=self.media_var,
                                value=self.media_btns[1],
                                command=self.sel
        )
        self.digital_btn.grid(row=5, column=1, sticky="w")

        self.print_btn = Radiobutton(
                            self.window,
                            text=self.media_btns[2],
                            variable=self.media_var,
                            value=self.media_btns[2],
                            command=self.sel
        )
        self.print_btn.grid(row=6, column=1, sticky="w")

        # Dynamically populate the Digital dropdown list
        self.digital_dir = AC_ProjectList(self.manager.digital_dir)

        # Dynamically populate the Print dropdown list
        self.print_dir = AC_ProjectList(self.manager.print_dir)

        self.digital_var = StringVar(self.window)
        self.digital_menu = OptionMenu(self.window, self.digital_var, *self.digital_dir.list)
        self.digital_menu.grid(row=5, column=1, columnspan=2, sticky="w", padx=self.padx*6)
        self.digital_menu.config(width=35, background=self.grey,
                                activebackground=self.active_blue,
                                activeforeground=self.disable_grey)

        self.print_var = StringVar(self.window)
        self.print_menu = OptionMenu(self.window, self.print_var, *self.print_dir.list)
        self.print_menu.grid(row=6, column=1, columnspan=2, sticky="w", padx=self.padx*6)
        self.print_menu.config(width=35, background=self.grey,
                            activebackground=self.active_blue,
                            activeforeground=self.disable_grey)

        # Set default button pressed for media_var and disable the drop downs
        self.broadcast_btn.select()
        self.digital_menu.config(state=DISABLED)
        self.print_menu.config(state=DISABLED)

        # Add separator for organization
        sep = ttk.Separator(self.window, orient="horizontal")
        sep.grid(row=7, column=0, columnspan=4, padx=self.padx, pady=self.btn_pady, sticky="we")

        # Open Projects Directory Location button
        self.open_btn_text = "Open Projects"
        self.open_btn = Button(self.window, text=self.open_btn_text,
                                command=lambda: self.openpath(self.media_var.get(),
                                self.get_media_path(self.media_var.get())))
        self.open_btn.config(bg=self.purple, fg=self.white, width=16,
                                activebackground=self.active_purple,
                                activeforeground=self.disable_grey)
        self.open_btn.grid(row=8, column=0, padx=self.padx, sticky="e")


        self.create_btn_text = "Create Project"
        self.create_btn = Button(self.window, text=self.create_btn_text, command=self.create_dir)
        self.create_btn.config(bg=self.blue, fg=self.white, width=self.btn_padx,
                                activebackground=self.active_blue,
                                activeforeground=self.disable_grey)
        self.create_btn.grid(row=8, column=1, sticky="w")


        self.close_btn = Button(self.window, text="Close", command=self.close_win)
        self.close_btn.config(bg=self.red, fg=self.white, width=self.btn_padx,
                            activebackground=self.active_red,
                            activeforeground=self.disable_grey)
        self.close_btn.grid(row=8, column=2, padx=self.padx, sticky="e")

    def close_win(self):
        """Callback to destroy the window."""
        self.window.destroy()

    def create_dir(self, *args):
        """Callback to Create a directory with the given parameters as the name of the directory.
        Copies and renames a template project for media files with same name."""
        # Decide which type of Media the directory belongs to
        media = self.media_var.get()
        parent_dir = self.get_media_path(media)

        # Grab the directory parent Location  EX. ..\Broadcast\Ford\
        # Grabs the current name for each part of the dir to build the location
        render_dir = os.path.join(self.manager.project_drive, media, parent_dir)
        brand_name = self.destination.get(ACTIVE)
        spot_name = self.manager.process_label(self.spot_entry.get())
        version_name = self.version_entry.get()
        month_number = self.month_entry.get()
        month_name = self.date.get_month(month_number)
        unique_name = (self.date.current_year, spot_name)
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

        self.manager.make_folders(render_dir, dir_name, folder_list)

        temp_file_name = 'Code_CampaignNumber_CampaignName_Version_001'

        project_path = os.path.join(render_dir, dir_name)

        ae_template = AC_Template(temp_file_name, 'aep', ae_dir, project_path)
        ae_template.copy_template(dir_name)

        pr_template = AC_Template(temp_file_name, 'prproj', pr_dir, project_path)
        pr_template.copy_template(dir_name)

        sizzle_dir = 'Broll'
        sizzle_temp_name = '{}_sizzle_reel'.format(self.brand_var.get())
        sizzle_template = AC_Template(sizzle_temp_name, 'txt', sizzle_dir, project_path)
        sizzle_template.copy_template(dir_name, rename=False)

        endcard_dir = 'Graphics'
        endcard_temp_name = '{}_endcard'.format(self.brand_var.get())
        endcard_template = AC_Template(endcard_temp_name, 'txt', endcard_dir, project_path)
        endcard_template.copy_template(dir_name, rename=False)

        lower_dir = 'Images'
        lower_temp_name = '{}_lower_thirds'.format(self.brand_var.get())
        lower_template = AC_Template(lower_temp_name, 'txt', lower_dir, project_path)
        lower_template.copy_template(dir_name, rename=False)

        # Open the file location in Explorer for convenience and confirmation
        self.openpath("{0}\\{1}".format(media, parent_dir), dir_name)

    def get_media_path(self, media):
        """Callback to return the media variable value."""
        media_dict = {
            "Print": self.print_var.get(),
            "Digital": self.digital_var.get(),
            "Broadcast": self.brand_var.get()
        }
        return media_dict.get(media, "Invalid media type")

    def on_brand_change(self,*args):
        """Callback for changing the Franchise name options to the destination folder."""
        self.destination.delete(0, END)
        for item in self.manager.brandname(self.brand_var.get()):
            self.destination.insert(END, item)
        self.destination.activate(0)

    def openpath(self,*args):
        """Callback to open the file location on the disk."""
        if len(args) > 1:
            subprocess.Popen('explorer {}\\{}\\{}'.format(self.manager.project_drive, args[0], args[1]))
        else:
            subprocess.Popen('explorer {}'.format(self.manager.default_dir))


    def sel(self):
        """Callback to select which medium this project is for."""
        if(self.media_var.get() == self.media_btns[1]):
            self.digital_menu.config(state = ACTIVE, bg=self.blue, fg=self.white)
        else:
            self.digital_menu.config(state = DISABLED, bg=self.grey)

        if(self.media_var.get() == self.media_btns[2]):
            self.print_menu.config(state = ACTIVE, bg=self.blue, fg=self.white)
        else:
            self.print_menu.config(state = DISABLED, bg=self.grey)


if __name__ == "__main__":
    window = Tk()
    manager = AC_PathManager()
    gui = AC_Magpype_GUI(window, manager)
    window.mainloop()
