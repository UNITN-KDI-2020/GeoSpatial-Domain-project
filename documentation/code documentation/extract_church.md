# Extract churchs

## Scope

The scope of the script is to download using the Overpass API all the church in province of Trento.

## How it work

Using the Overpass library, we ran the following query:

```
[out:json][timeout:25];
// fetch area “Trentino” to search in
( area["name"="Provincia di Trento"]; )->.searchArea;
(
  // query part for: “building=yes”
  node["building"="yes"]["amenity"="place_of_worship"](area.searchArea);
  way["building"="yes"]["amenity"="place_of_worship"](area.searchArea);
  relation["building"="yes"]["amenity"="place_of_worship"](area.searchArea);
);
// print results
out body;
>;
out skel qt;
```

The result was then saved inside a GeoJSON file.