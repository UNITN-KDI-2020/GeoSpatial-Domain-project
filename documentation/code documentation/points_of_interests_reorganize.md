# Point of interests reorganize

## Scope
The scope of the script is to copy all the files about the points of interest from the directory with the data to another where the metadata will locate and correct the naming.

## How it work

The script list all the files present inside the source directory then for each file if CLASSES is present inside the name, the script copy it to the destination folder changing the name and remove the original file.