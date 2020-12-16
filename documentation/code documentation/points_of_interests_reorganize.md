# Point of interests reorganize

## Scope
The scope of the script is to download from the opendati Trentino portal the datas about the point of interest that each city publish on the portal.

## How it work

The script use lxml to parse the HTML content of the page and requests to download the pages content. To download the data it first check the result of the search at the URL `https://dati.trentino.it/dataset?tags=luoghi+e+punti+di+interesse&page={i}` where `{i}` is a integer going from `1` to `9`, that correspond to how many pages of result are shows. Then for each datasets found inside the search result, it access the specific dataset page, here it parse the HTML to recover the point of interest for the given particular city. Consider the Data Trentino portal it is not stable we introduce inside some wait time and some check so that the script can wait that the Data Trentino platform return available.