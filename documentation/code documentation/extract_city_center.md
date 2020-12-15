# Extract city centers

## Scope

The scope of the script is to download using the Overpass API all the city centers in province of Trento.

## How it work

Using the Overpass library, we ran the following query:

```
[out:json][timeout:25];
// fetch area "Trentino" to search in
( area["name"="Provincia di Trento"]; )->.searchArea;
(
  // query part for: "building=yes"
  node["admin_level"=8](area.searchArea);
  way["admin_level"=8](area.searchArea);
  relation["admin_level"=8](area.searchArea);
);
// print results
out body;
>;
out skel qt;
```

The result was then saved inside a GeoJSON file. The result return both the limit of the city and the city centers that for a specificity of the territory can be in some more than one.