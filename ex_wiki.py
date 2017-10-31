import urllib2
import requests
# import helpers
import pdb

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

prefix = '''
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
'''

url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'


# query5 asks for official_language entity pair that must have start time or end time.
query5 =  prefix + '''SELECT ?entity1 ?entity1Label ?entity2 ?entity2Label ?start ?end WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?entity1 p:P37 ?statement.
  ?statement ps:P37 ?entity2.
  OPTIONAL{
             ?statement pq:P580 ?start.
    }
  OPTIONAL{
             ?statement pq:P582 ?end.
    }
  FILTER(BOUND(?start) || BOUND(?end)).
}
}'''

# query6 asks for people who stays in some place and got left with start and end time.
query6 = prefix + '''SELECT ?person ?personLabel ?location ?locationLabel ?start ?end WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?person p:P551 ?statement.
  ?statement ps:P551 ?location;
             pq:P580 ?start;
             pq:P582 ?end.
}'''


def save_properties(prefix):

    # query1/2/3/4 asks for properties that allows start time / end time

    mandatory = 'Q21510856'
    optional = "Q21510851"

    start = prefix + '''
    SELECT ?property ?propertyLabel WHERE {
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
      ?property p:P2302 ?statement.
      ?statement ps:P2302 wd:'''

    mid = '''.
    ?statement pq:P2306 wd:'''

    end = '''.
    }'''

    start_time = 'P580'
    end_time = 'P582'

    query1 = start + mandatory + mid + start_time + end
    query2 = start + optional + mid + start_time + end
    query3 = start + mandatory + mid + end_time + end
    query4 = start + optional + mid + end_time + end

    p_qs = [query1, query2, query3, query4]


    time_properties = []
    for query in p_qs:
        time_properties.append(requests.get(url, params={'query': query, 'format': 'json'}).json())

    properties = []

    # process the properties with start_time and end_time seperately.
    for tps in time_properties:
        for item in tps['results']['bindings']:
            properties.append({
                'url':item['property'],
                'property':item['property']['value'].split('/')[-1],
                'name':item['propertyLabel']['value']
            })

    properties = pd.DataFrame(properties).drop_duplicates()
    print(properties)
    path = "./origin_data/"
    with open(path+'properties','w') as f:
        properties.to_csv(f, encoding='utf-8')
    print(properties)
    return properties


def entities(prefix, properties):
    start = prefix + '''SELECT ?entity1 ?entity1Label ?entity2 ?entity2Label ?start ?end WHERE {
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }'''

    end = '''OPTIONAL{
                 ?statement pq:P580 ?start.
        }
      OPTIONAL{
                 ?statement pq:P582 ?end.
        }
      FILTER(BOUND(?start) || BOUND(?end)).
    }
    LIMIT 100
    '''

    entity = []

    # got for loop of each row
    for i in range(properties.shape[0]):
        prop = properties.iloc[i]['property']
        prop_name = properties.iloc[i]['name']
        print(prop)
        query = start + "?entity1 p:" + prop + " ?statement.\n" + "?statement ps:" + prop + " ?entity2.\n" + end
        try:
            response = requests.get(url, params={'query': query, 'format': 'json'}, timeout=2).json()
        except requests.exceptions.ReadTimeout:
            print('Passed!')
            continue
        except:
            pdb.set_trace()
            continue
        for item in response['results']['bindings']:
            entity.append({
                'relation': prop,
                'entity1': item['entity1']['value'],
                'entity1Label': item['entity1Label']['value'],
                'entity2': item['entity2']['value'],
                'entity2Label': item['entity2Label']['value'],
                'start_time': item['start']['value'] if item.get('start') else None,
                'end_time': item['end']['value'] if item.get('end') else None
            })
    entity = pd.DataFrame(entity)
    pdb.set_trace()
    return entity


if __name__ == "__main__":
    # properties = save_properties(prefix)
    properties = pd.read_csv("./origin_data/properties")
    entity = entities(prefix, properties)


# pdb.set_trace()

