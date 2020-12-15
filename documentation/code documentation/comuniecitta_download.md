# School download

## Scope

The scope of the script is to scrape the list of high schools from the Comuni and Città portal.

## How it work

The script use webdriver and beautiful soup to extract all the schools present at the page [https://www.comuniecitta.it/scuole-secondarie-di-secondo-grado/comune-di-trento-22205](https://www.comuniecitta.it/scuole-secondarie-di-secondo-grado/comune-di-trento-22205). The content of the page recoveried by webdriver is then parsed by BeatifulSoup that extract the schools presents. Then for each school present in the page the script load the detail page and extract from it the details about the course of study available.
