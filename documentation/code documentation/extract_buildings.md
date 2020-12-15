# Extract buildings

## Scope

The scope of the script is to download using the Overpass API all the buildings in province of Trento.

## How it work

Considering the size of the dataset it is necessary to extract the data individually for each city present in Trentino. For this reason we hardwire inside all the city of Trentino at the present date (15/12/2020). Then we run the following query for each city on the list, replacing `{}` with the name of the city to search:

```
[out:json][timeout:25];
// fetch area “Trentino” to search in
( area["name"="Provincia di Trento"]; )->.externalBoundary;
( area["name"="{}"]; )->.searchArea;
(
  // query part for: “building=yes”
  node["building"="yes"](area.searchArea)(area.externalBoundary);
  way["building"="yes"](area.searchArea)(area.externalBoundary);
  relation["building"="yes"](area.searchArea)(area.externalBoundary);
);
// print results
out body;
>;
out skel qt;
```

The result was then saved inside a GeoJSON file.