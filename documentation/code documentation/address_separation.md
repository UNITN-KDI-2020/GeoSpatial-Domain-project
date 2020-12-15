# Address Separation

## Scope

The scope of this script is to divide an address in the Italian format, into it's various components

## How it work

First the script list all the files inside the datasets folder. All our datasets was transformed in json, so it exclude from the datasets to transform the ones that are not in the form of a json file and the ones present into the exclusion list.

Then cycle for each record present in each dataset, check if a address field is present and proceed to try to parse it.

If the parse success the address components, substitute the address field inside the record, otherwise the address is inserted inside the additional information field.

The first step to parse it is to found the city, we use the list of all the 7903 cities present in Italy and scan the string for obtain a correspondance. Then the city is removed from the address. The string is then split in words. The system inside each words check if is a prefix (comparing it with a given list of prefix), or if it is a valid postal code (CAP) or house number the remaining part became the street name.