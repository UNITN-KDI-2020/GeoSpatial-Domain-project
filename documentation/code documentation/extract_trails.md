# Extract trails

## Scope

The scope of the script is to download using the Overpass API all the trails in province of Trento.

## How it work

Using the Overpass library, we ran the following query:

```
[out:json][timeout:25];
// fetch area “Trentino” to search in
( area["name"="Provincia di Trento"]; )->.searchArea;
// gather results
(
  // query part for: “highway=path”
  node["highway"="path"](area.searchArea);
  way["highway"="path"](area.searchArea);
  relation["highway"="path"](area.searchArea);
);
// print results
out body;
>;
out skel qt;
```

The result was then saved inside a GeoJSON file.