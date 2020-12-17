# School Allineation

## Scope

The main scope of the script is to align the coordinate format to the standard `epsg:4326` used inside the ontology. It also correct the naming of various field so the notation correspond to the ones used in the other datasets.

## How it work

The script list all the schools datasets contain inside the `schools` folder in the `data` directory of the Informal phase. Then it parse the filename to discover what type of schools is watching. Then for each record inside the file it convert the coordinate to the `epsg:4326` format. Then it correct the naming of the address fields and add the school type. The results are then saved inside a json file.