# Count the available attribute

## Scope

The scope of the script is to filter from the files, all the field not neccesary for populate the ontology.

## How it work

The script given a config file, with a format like the following:

```json
{
	"skislopes.json": {
		"iterator": "features",
		"props": [
			"properties.name",
			"properties.@id",
			"properties.piste:type",
			"properties.piste:difficulty",
			"geometry"
		]
	},
}
```

The index of the root object contain the name of the file to clean. Inside each object the field `iterator` contain the element to cycle to recovery all the records to clean. Then for each record found using the iterator remove the field not in the `props` list. The system can work similarly also with CSV files but given that there is only one level the iterator field is not necessary. The CSV file is converted for future elaboration into JSON format.

A similar thing is made for the files inside the folders `luoghi_e_punti_di_interesse_per_comune` and `building`.