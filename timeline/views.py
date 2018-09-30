from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
# Create your views here.
def index(request):
	query_str = get_query()
	sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	result = results['results']['bindings']
	print(type(result))
	return render(request, 'timeline/file.html',{'content':result})


def get_query():
	return ("""
	SELECT ?item ?itemLabel ?launchdate (SAMPLE(?image) AS ?image)
	WHERE
	{
		?item wdt:P31 wd:Q26529 .
	    ?item wdt:P619 ?launchdate .
		SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
	    OPTIONAL { ?item wdt:P18 ?image. }

	    ?item wdt:P137 wd:Q23548.
	}
	GROUP BY ?item ?itemLabel ?launchdate
	""")