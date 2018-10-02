from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
# Create your views here.

def get_query():
	query1 = """
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
	"""

	query = """
	SELECT DISTINCT ?item ?itemLabel ?launchdate (SAMPLE(?image) AS ?image)
	WHERE
	{
		{
          ?item wdt:P31 wd:Q26529 .
         }
        UNION
        {
          ?item wdt:P31 wd:Q1378139 
        }
        UNION
        {
          ?item wdt:P31 wd:Q2133344 
        }
        UNION
        {
          ?item wdt:P31 wd:Q40218
        }     
	    ?item wdt:P619 ?launchdate .
		?item rdfs:label ?itemLabel. 
	    OPTIONAL { ?item wdt:P18 ?image. }
        FILTER(LANG(?itemLabel) ="en") .
        FILTER(!CONTAINS(LCASE(?itemLabel), "\'"@en)). 
	}
	GROUP BY ?item ?itemLabel ?launchdate
	"""
	return query

def get_predicate_query():
	query = """
	SELECT DISTINCT ?p ?o
	WHERE
	{
		?item wdt:P31 wd:Q26529 .
		?item wdt:P137 wd:Q23548 .
		?item ?p ?o.
	}
	"""
	return query

def exec_query():
	query_str = get_query()
	sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	result = results['results']['bindings']
	return result

def get_predicates_and_objects():
	query_str = get_predicate_query()
	sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	result_uris = results['results']['bindings']
	res_predicates = []
	for uri in result_uris:
		res_predicates.append(uri['p']['value'])
	res_objects = []
	for uri in result_uris:
		res_objects.append(uri['o']['value'])
	return (res_predicates,res_objects)


def index(request):
	predicates,objects = get_predicates_and_objects()
	result = exec_query()
	return render(request, 'timeline/file.html',{'content':result, 'predicates': predicates, 'objects':objects})


