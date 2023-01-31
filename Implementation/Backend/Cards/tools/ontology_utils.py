from pprint import pprint

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph

sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)


def poke_types_ontology(g, json_entity, ontology_entity):
    for t in json_entity.get("types", []):
        dbr = POKEMON_TYPE_DBPEDIA.get(t)
        type_node = EX["type_" + t]

        if dbr is not None:
            g.add((type_node, RDFS.subClassOf, DBR[dbr]))
        g.add((type_node, RDF.type, POKE.Type))
        g.add((type_node, RDFS.label, Literal(t)))
        g.add((ontology_entity, POKE["type"], type_node))


def format_name(source):
    return source.replace(" ", "_").replace("'", "")


def query_dbpedia_by_keyword(text, target, return_url=False):
    words = []
    target = re.split("\\W+", target)
    for t in re.split("\\W+", text):
        if len(t) > 1:
            words += ["'" + t + "'"]

    sparql.setQuery(
        '''
            define input:ifp "IFP_OFF" select ?s1 as ?c1, (bif:search_excerpt (bif:vector (%s), ?o1)) as ?c2, ?sc, ?rank, ?g where {{{
                select ?s1, (?sc * 3e-1) as ?sc, ?o1, (sql:rnk_scale (<LONG::IRI_RANK> (?s1))) as ?rank, ?g where {
                    quad map virtrdf:DefaultQuadMap {
                        graph ?g {
                            ?s1 ?s1textp ?o1 . ?o1 bif:contains "(%s)" option (score ?sc) .
                        }
                    }
                }
                order by desc (?sc * 3e-1 + sql:rnk_scale (<LONG::IRI_RANK> (?s1))) limit 500 offset 0
            }}}
        ''' % (", ".join(words), " AND ".join(words)))

    try:
        ret = sparql.queryAndConvert()

        for binding in ret["results"]["bindings"]:
            for w in target:
                if w.lower() in binding["c1"]["value"].lower():
                    if return_url:
                        return binding["c1"]["value"]
                    return binding["c1"]["value"].split("/")[-1]
    except Exception as ex:
        print("DBPEDIA QUERY KEYWORD EXCEPTION: ", str(ex))
    return None


from ontologies import *


def cards_type_build_ontology(g):
    g.bind(PREFIX_EX, EX)
    g.bind("dbo", DBO)

    for t in CARD_TYPES_CHART.keys():
        type_node = EX["type_" + t.name]

        for k in CARD_TYPES_CHART.get(t, []):
            g.add((type_node, DBO.defeat, EX["type_" + k.name]))
    return g


def cards_build_ontology():
    g = cards_type_build_ontology(Graph())
    g = star_trek_build_ontology(g)
    g = star_wars_build_ontology(g)
    g = pokemon_build_ontology(g)
    g = marvel_build_ontology(g)

    # g.serialize(destination="data/ontology/final.ttl")
    return g


def cards_get_names(g):
    try:
        return [str(x[0]) for x in list(g.query(
            '''
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix dbr: <http://dbpedia.org/resource/>
                select ?name where { ?card rdf:type dbr:Playing_card . ?card rdfs:label ?name . }
            '''
        ))]
    except Exception as ex:
        print("EXCEPTION CARD GET NAMES ", ex)
        return list()


def cards_get_universes(g):
    try:
        return [str(x[0]) for x in list(g.query(
            '''
                prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix dbr: <http://dbpedia.org/resource/>
                prefix foaf: <http://xmlns.com/foaf/0.1/>
                prefix gada: <https://gada.cards.game.namespace.com/>
                
                select distinct ?universe where {
                    ?card rdf:type dbr:Playing_card .
                    ?card foaf:member ?universe . 
                }
            '''
        ))]
    except Exception as ex:
        print("EXCEPTION CARD GET NAMES ", ex)
        return list()


def id_to_json_ld(g, entity_id, context):
    if type(entity_id) is str:
        entity_id = URIRef(entity_id)

    temp_g = Graph()
    for rdf_tuple in list(g.query(
            "select ?s ?p ?o where { ?s ?p ?o . }",
            initBindings=dict(s=entity_id)
    )):
        temp_g.add(rdf_tuple)

    try:
        result = json.loads(temp_g.serialize(format='json-ld', context=context))
        if type(result) is list:
            return result[0]
        return result
    except Exception as ex:
        print("ID TO JSON LD EXCEPTION ", str(ex))
        return None


def card_name_to_id(g, card_name):
    try:
        return list(g.query(
            '''
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix dbr: <http://dbpedia.org/resource/>
                select ?card where { ?card rdf:type dbr:Playing_card . ?card rdfs:label ?name . }
            ''',
            initBindings=dict(name=Literal(card_name))
        ))[0][0]
    except:
        return None


def card_name_to_universe(g, card_name):
    try:
        return list(g.query(
            '''
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                prefix dbr: <http://dbpedia.org/resource/>
                prefix foaf: <http://xmlns.com/foaf/0.1/>
                prefix owl: <http://www.w3.org/2002/07/owl#>

                select ?univ_id where { 
                    ?card rdf:type dbr:Playing_card . ?card rdfs:label ?name . 
                    ?card foaf:member ?univ . ?univ owl:sameAs ?univ_id 
                }
            ''',
            initBindings=dict(name=Literal(card_name))
        ))[0][0]
    except:
        return None


def cards_get_json_ld(g=None, cards_names=None):
    if g is None:
        g = Graph()
        g.parse('data/ontology/marvel/final.ttl', format="ttl")

    json_lds = []
    if cards_names is None:
        cards_names = cards_get_names(g)
    for card_name in cards_names:
        univ = card_name_to_universe(g, card_name)
        js_ld = None

        if univ == DBR.Star_Trek:
            js_ld = star_trek_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld)
        elif univ == DBR.Star_Wars:
            js_ld = star_wars_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld)
        elif univ == DBR.Pokémon:
            js_ld = pokemon_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld)
        elif univ == DBR.Marvel_Universe:
            js_ld = marvel_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld)

        if js_ld is not None:
            # pprint(js_ld)
            # print("\n========================")
            json_lds.append(js_ld)
    return json_lds


def cards_get_json(g=None, cards_names=None):
    if g is None:
        g = Graph()
        g.parse('data/ontology/star_wars/final.ttl', format="ttl")

    json_list = []
    if cards_names is None:
        cards_names = cards_get_names(g)
    for card_name in cards_names:
        univ = card_name_to_universe(g, card_name)
        js_result = None

        if univ == DBR.Star_Trek:
            js_result = star_trek_get_json(star_trek_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld))
        elif univ == DBR.Star_Wars:
            js_result = star_wars_get_json(star_wars_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld))
        elif univ == DBR.Pokémon:
            js_result = pokemon_get_json(pokemon_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld))
        elif univ == DBR.Marvel_Universe:
            js_result = marvel_get_json(marvel_get_json_ld(g, card_name_to_id(g, card_name), id_to_json_ld))

        if js_result is not None:
            # pprint(js_result)
            # print("\n========================")
            json_list.append(js_result)
    return json_list


def get_card_deck(deck_size, deck_offset=0, randomize=False, g=None):
    if g is None:
        g = Graph()
        g.parse('data/ontology/gada_cards.ttl', format="ttl")

    if type(deck_size) is not int or deck_size <= 0:
        deck_size = 100
    if type(randomize) is not bool:
        randomize = False
    if type(deck_offset) is not int or deck_size < 0:
        deck_offset = 0

    try:
        if randomize:
            cards = []
            extra_add = 0

            universes = cards_get_universes(g)
            for univ in universes:
                batch_size = deck_size // len(universes) + 1 + extra_add

                current_cards = [str(x[0]) for x in list(g.query(
                    '''
                        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        prefix dbr: <http://dbpedia.org/resource/>
                        prefix foaf: <http://xmlns.com/foaf/0.1/>
                        prefix gada: <https://gada.cards.game.namespace.com/>

                        select ?name where { 
                            ?card rdf:type dbr:Playing_card .
                            ?card rdfs:label ?name . 
                            ?card foaf:member %s .
                            bind(sha512(concat(str(rand()), str(?name))) as ?random) 
                        } order by ?random
                        limit %s
                    ''' % ("gada:" + univ.split("/")[-1], batch_size)
                ))]

                cards += current_cards
                if len(current_cards) <= batch_size:
                    extra_add = batch_size - len(current_cards)

            random.shuffle(cards)
            return cards[0:deck_size]
        else:
            return [str(x[0]) for x in list(g.query(
                '''
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    prefix dbr: <http://dbpedia.org/resource/>
                    select ?name where { 
                        ?card rdf:type dbr:Playing_card .
                        ?card rdfs:label ?name . 
                    }
                    limit %s
                    offset %s
                ''' % (deck_size, deck_offset)
            ))]
    except Exception as ex:
        print("EXCEPTION CARD GET NAMES ", ex)
        return list()
