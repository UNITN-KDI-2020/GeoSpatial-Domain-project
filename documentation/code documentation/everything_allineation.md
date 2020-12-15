# Allineation

## Scope

The scope of the script is to align the different geospatial coordinate system to a unique coordinate system in our case the `epsg:4326`. This script is the result of the formal phase so for some class we decide to also remove some field that we do not longer use.

## How it work

The script scan the directory with the dataset, and depending on the dataset it apply various types of action:

- convert the coordinate system
- delete fields that we decide to ignore
- compute the area of the record (like for computing the area of the supermarket)
- compute the distance (used for example during for the bicycle path)
- correct the enumerated type inside the fields
- if the position of a location is a shape compute the center point

The algorithm also insert the metadata file the field about the GeoShape type (point, polygon, line) and correct the names of the field.