# Ski Slope Link

## Scope

The main scope of the script is to assign each ski slope to the corresponding the ski area.

## How it work

The script read all skiareas and skislopes from the respective datasets files. Then for each skiarea it compute the mean point of the slope coordinate and using this point try to find where ski area it belongs. Then it pass all the ski area and for each ski area find the area where the distance between the center point of the slope and the center point of the area is lowered. It then check if the slopes coordinate intersect with the found area. If yes, the match is positive, and the script add a field with the relation. The results are then saved in a JSON file.