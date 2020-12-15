# Building allineation

## Scope

The scope of the script is to group together all the various building file created by the `extract-buildings.py` script. During this process it also change the name of address's field and compute the central point of each buidling.

## How it work

The script scan the directory that contain all the buildings, divided by city. For each file found inside it cycle over the records and compute the average position of each building. To compute the position it take all the points that compose the border of the building and average over them. It also add the name of the city from which it was extracted to each building record, the last operation is to change the name of the address field.
