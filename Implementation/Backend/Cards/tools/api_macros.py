from rdflib import Graph

SERVER_PORT = '5053'

GADA_ONTOLOGY = Graph()
GADA_ONTOLOGY.parse('data/ontology/gada_cards.ttl', format="ttl")
