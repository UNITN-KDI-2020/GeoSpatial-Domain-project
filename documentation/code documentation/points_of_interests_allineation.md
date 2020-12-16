# Point of interests allineation

## Scope

The scope of the script is to split the various datasets that the cities make available with the points of interests inside the city border. The result is a series of files that contain:

- theaters
- churches
- doctor's offices
- eldery centers
- bars
- sport facilities

## How it work

The script read all the points of interests datasets, from the folder. Then for each point of interest check based on the name in which of the category listed before insert the record. At the end the category are exported as JSON file.