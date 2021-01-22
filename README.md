# AC-RSPipeline -- A Custom Projects Directory Management Framework

This is a project directory creation framework that I made using Tkinter to learn how to build GUIs in Python. It allows you to quickly access the directory on your drive, pointing to the location the drop down parameters are pointing to. The lists are populated with existing folders in the pointed locations.

This script allows the user to create project folder with very specific parameters to place it on the server with very orgainized naming convention that allows for ease of identification. Every folder will be unique to the location.

## Some highlights for this project

- Creates a project directory that is named in a very organized way
- Copies a template project from assigned asset drive into pointed directory location and renames it to the project name
- Process the label name to remove white space and capitalcase the string text
- Will prefix the label name with the current year to add unique names in the folder
- Will suffix the label with a 3-padding version number
- Uses logic to decide where the final directory should go according to the pointed directory
- Uses color highlighting to show important entry fields in the GUI
- Dynamically populate listbox depending on the selected parameter for the dropdown
- Button to open the file location in Explorer for quick navigation
- Convenience Button to close the GUI window
- Button to create the directory
