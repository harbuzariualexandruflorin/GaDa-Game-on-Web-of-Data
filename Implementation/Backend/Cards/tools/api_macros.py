# from rdflib import Graph
# GADA_ONTOLOGY = Graph()
# GADA_ONTOLOGY.parse('data/ontology/gada_cards.ttl', format="ttl")

from rdflib.plugins.stores import sparqlstore

SERVER_PORT = '5053'

FUSEKI_ENDPOINT = 'http://localhost:3030/gada_set/query'
store = sparqlstore.SPARQLStore()
store.open(FUSEKI_ENDPOINT)
GADA_ONTOLOGY = store
