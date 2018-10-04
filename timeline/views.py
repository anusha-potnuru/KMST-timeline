from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from timeline.forms import filter_form
from datetime import datetime
from dateutil.parser import parse
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


def exec_query():
	query_str = get_query()
	sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	result = results['results']['bindings']
	return result

def index(request):
	launchsites = []
	launchsite_list = [(None,'Select')]
	result = exec_query()
	for r in result:
		if('launchsite' in r):
			launchsites.append(r['launchsite']['value'])
	launchsites = list(set(launchsites))
	for i in range(len(launchsites)):
		launchsite_list.append((launchsites[i],launchsites[i]))

	if request.method == 'POST':
		form = filter_form(launchsite_list,request.POST)
		if form.is_valid():
			launchsite_selected = form.cleaned_data['launchsite']
			mission_type = form.cleaned_data['typeofmission']
			launchdate_from = form.cleaned_data['launchdate_from']
			launchdate_to = form.cleaned_data['launchdate_to']
			mission_duration_min = form.cleaned_data['mission_duration_min']
			mission_duration_max = form.cleaned_data['mission_duration_max']
			# print(launchsite_selected)
			# print(mission_type)
			# print(type(launchdate_from))
			# print(launchdate_to)
			# print(mission_duration_min)
			# print(mission_duration_max)
			print(launchsite_selected)
			for r in result:
				if(launchsite_selected is not ''):
					if('launchsite' not in r or r['launchsite']['value'] != launchsite_selected):
						if('launchsite' in r):
							print('removed '+ r['launchsite']['value'])
						result.remove(r)
						continue
				if(mission_type != 0):
					if(mission_type == 1):
						if(r['crews']['value'] != ''):
							result.remove(r)
							continue
					else:
						if(r['crews']['value'] == ''):
							result.remove(r)
							continue
				if(launchdate_from is not None):
					launchdate_from_str = r['launchdate']['value'].split(sep='T')[0]
					launchdate_from_parsed = datetime.strptime(launchdate_from_str,'%Y-%m-%d')
					if(launchdate_from_parsed<launchdate_from):
						result.remove(r)
						continue
				if(launchdate_to is not None):
					launchdate_from_str = r['launchdate']['value'].split(sep='T')[0]
					launchdate_from_parsed = datetime.strptime(launchdate_from_str,'%Y-%m-%d')
					if(launchdate_from_parsed>launchdate_to):
						result.remove(r)
						continue

	else:
		form = filter_form(launchsite_list = launchsite_list)
	return render(request, 'timeline/file.html',{'form':form,'content':result})


# def filter(request):
# 	launchsite_list = [(0,'Select')]
# 	launchsites = []
# 	result = exec_query()
# 	for r in result:
# 		if('launchsite' in r):
# 			launchsites.append(r['launchsite']['value'])
# 	launchsites = list(set(launchsites))
# 	for i in range(len(launchsites)):
# 		launchsite_list.append((i+1,launchsites[i]))
# 	f = filter_form(launchsite_list = launchsite_list)
# 	return render(request,'timeline/temp.html', {'form':f})