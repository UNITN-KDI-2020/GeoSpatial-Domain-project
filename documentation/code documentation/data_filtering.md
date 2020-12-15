# Count the available attribute

## Scope

The scope of the script is to filter from the files, all the field not neccesary for populate the ontology.

## How it work

The script given a config file, for each record inside extract the fields present. For each field the correspond value inside a dictionary is increment (or set to 1 if the program do not have see the field before). After all the record are counted then it is possible to compare each field present inside the dictionary with the total number of record present inside the file and output the percentage of records present.