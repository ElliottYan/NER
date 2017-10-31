# can have the alias by request the entity's page in json format.
# e.g. Columbia
# a['entities']['Q739']['aliases']['en']
"""
[{'language': 'en', 'value': 'co'},
 {'language': 'en', 'value': 'United States of Colombia'},
 {'language': 'en', 'value': 'República de Colombia'},
 {'language': 'en', 'value': 'Republic of Colombia'},
 {'language': 'en', 'value': 'Republica de Colombia'}]
 """

# for extracting the wiki pages.
# a['entities']['Q6199']['sitelinks']['enwiki']




query_tmp = '''SELECT ?otherName ?language ?languageLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?language wdt:P31 wd:Q6256.
}
LIMIT 100'''


"""
SELECT ?entity1 ?entity1Label ?entity2 ?entity2Label ?start ?end WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?entity1 p:P2632 ?statement.
  ?statement ps:P2632 ?entity2.
  OPTIONAL{
             ?statement pq:P580 ?start.
    }
  OPTIONAL{
             ?statement pq:P582 ?end.
    }
  FILTER(BOUND(?start) || BOUND(?end)).
}
"""