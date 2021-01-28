# AC-Magpype -- A Custom Projects Directory Management Framework

This is a project directory creation framework that I made using Tkinter to learn how to build GUIs in Python. It allows you to quickly access the directory on your drive, pointing to the location the drop down parameters are pointing to. The lists are populated with existing folders in the pointed locations.

This script allows the user to create project folder with very specific parameters to place it on the server with very orgainized naming convention that allows for ease of identification. Every folder will be unique to the location.

## Some highlights for this project

- Creates a project directory structure that is named in a very organized way
- Copies a template project file (i.e. AE, Premiere, MP4, etc.) from assigned asset drive into pointed directory location and renames it to the project name
- Process the label name to remove white space and capitalcase the string text
- Will prefix the label name with the current year to add unique names in the folder
- Will suffix the label with a 3-padding version number
- Uses logic to decide where the final directory should go according to the pointed directory
- Uses color highlighting to show important entry fields in the GUI
- Dynamically populate with existing projects on the non-default project locations
- Button to open the file location in Explorer for quick navigation
- Convenience Button to close the GUI window
- Button to create the directory

## Running the script

If you run ac_magpype_gui.py from main, the script will run and build the GUI. It uses ac_manager as to control certain functionalities, you can replace the manager when passing to the contstructor for custom layouts. However so far, the script still relies on it for certain functionalities to run. These functionalities are mostly optional however, and will be more modular in future release. 
