# Metadata filtering

## Scope

The scope of the script is to filter the metadata file, from one phase to the other during the fields filtering.

## How it work

The script read the JSON file that contain the data and list the fields that continue to be used inside it. Then it read all the fields listed inside the metadata file and if some of this fields are not used anymore they are removed. At the end the modification was saved on the specified destination folder.