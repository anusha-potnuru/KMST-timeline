from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
# Create your views here.

def get_query():
	query = """
	SELECT DISTINCT ?item ?itemLabel ?launchdate (GROUP_CONCAT(distinct ?crewLabel; SEPARATOR=", ") AS ?crews)  (SAMPLE(?image) AS ?image) ?wikipedia ?launchsite WHERE {
		{ ?item wdt:P31 wd:Q26529. }
		UNION
		{ ?item wdt:P31 wd:Q1378139. }
		UNION
		{ ?item wdt:P31 wd:Q2133344. }
		UNION
		{ ?item wdt:P31 wd:Q40218. }
		UNION
		{ ?item wdt:P31 wd:Q752783. }
		UNION
		{ ?item wdt:P137 wd:Q23548. }
		UNION
		{ ?item wdt:P1427 wd:Q845774. }
		UNION
		{ ?item wdt:P31 wd:Q5916. }
		?item wdt:P619 ?launchdate.
		?item rdfs:label ?itemLabel.
		OPTIONAL { ?item wdt:P18 ?image. }
		OPTIONAL{
		?item wdt:P1029 ?crew .
		?crew rdfs:label ?crewLabel.
		FILTER((LANG(?crewLabel)) = "en")
        FILTER(!CONTAINS(LCASE(?crewLabel), "'"@en))
        }
		OPTIONAL {
		  ?wikipedia schema:about ?item .
		  ?wikipedia schema:inLanguage "en" .
		  FILTER (SUBSTR(str(?wikipedia), 1, 25) = "https://en.wikipedia.org/")
		}
        OPTIONAL{
          ?item wdt:P1427 ?lsite .
          ?lsite rdfs:label ?launchsite .
          FILTER((LANG(?launchsite)) = "en")
          FILTER(!CONTAINS(LCASE(?launchsite), "'"@en))
        }
		FILTER((LANG(?itemLabel)) = "en")
		FILTER(!CONTAINS(LCASE(?itemLabel), "'"@en))
	}
	GROUP BY ?item ?itemLabel ?launchdate  ?wikipedia ?launchsite
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
	print(result[0])
	launchsites = []
	for r in result:
		if('launchsite' in r):
			launchsites.append(r['launchsite']['value'])
	launchsites = list(set(launchsites))
	return render(request, 'timeline/file.html',{'content':result,'launchsites':launchsites})


