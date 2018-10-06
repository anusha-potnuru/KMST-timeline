# KMST-timeline

Timeline view of NASA space missions

The backend is built using django framework.

The data for the timeline is obtained via a sparql query to [wikidata](https://query.wikidata.org/sparql). 
The query is processed using [SPARQLWrapper](https://rdflib.github.io/sparqlwrapper/) library.

This data is then processed to obtain relevant information and passed to [histropediaJS](http://histropedia.com/histropediajs/index.html) tool for rendering the timeline. 

Finally the app is uploaded to [Heroku](https://www.heroku.com) cloud platform service.

Visit https://kmst-timeline.herokuapp.com to view
