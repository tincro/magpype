# Custom Projects Directory Manager

**createDirectory.py** is a project directory creator that I made using Tkinter to learn how to build GUI in Python. It allows you to quickly access the directory on your drive, pointing to the location the drop down parameters are pointing to. The lists are populated with existing folders in the pointed locations.

This script allows the user to create project folder with very specific parameters to place it on the server with very orgainized naming convention that allows for ease of identification. Every folder will be unique to the location.

## Features for createDirectory.py:

- Creates a project directory that is named in a very organized way
- Copies a template project from Asset drive into pointed directory location and renames it
- Process the label name to remove white space and capitalcase the string text
- Will prefix the label name with the current year to add unique names in the folder
- Will suffix the label with a pad3 version number
- Uses logic to decide where the final directory should go according to the pointed directory
- Uses color highlighting to show important entry fields in the GUI
- Dynamically populate listbox depending on the selected parameter for the dropdown
- Button to open the file location in Explorer for quick navigation
- Button to close the GUI window
- Button to create the directory
