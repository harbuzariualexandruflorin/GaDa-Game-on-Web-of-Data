from rdflib import URIRef, Literal, OWL, SSN, RDFS
from rdflib.namespace import FOAF, RDF, SDO, GEO, XSD

from tools.common_utils import *
from tools.ontology_macros import *
from tools.ontology_utils import format_name, query_dbpedia_by_keyword, poke_types_ontology


def marvel_build_ontology(g, limit=None):
    g.bind("dbo", DBO)
    g.bind("dbr", DBR)
    g.bind(PREFIX_EX, EX)
    g.bind("foaf", FOAF)
    g.bind("geo", GEO)
    g.bind("owl", OWL)
    g.bind("poke", POKE)
    g.bind("rdfs", RDFS)
    g.bind("sdo", SDO)
    g.bind("ssn", SSN)
    g.bind("xsd", XSD)

    all_characters = load_json_file_to_dict("data/json/marvel/final.json")
    universe = EX["univ_Marvel"]
    g.add((universe, RDFS.label, Literal("Marvel")))
    g.add((universe, OWL.sameAs, DBR.Marvel_Universe))

    index = 0
    for character in all_characters["characters"]:
        index += 1
        if limit is not None and index > limit:
            break

        entity = EX["card_" + format_name(character["name"])]
        g.add((entity, FOAF.member, universe))
        dbr = query_dbpedia_by_keyword("marvel character " + character["name"], character["name"])
        if dbr is not None:
            print(dbr)
            g.add((entity, RDFS.seeAlso, DBR[dbr]))

        g.add((entity, RDF.type, DBR.Playing_card))
        g.add((entity, RDF.type, DBC.Lists_of_fictional_characters))
        g.add((entity, RDF.type, DBC.Lists_of_Marvel_Comics_characters))

        g.add((entity, RDFS.label, Literal(character["name"])))
        g.add((entity, FOAF.img, URIRef(character["avatar"])))
        g.add((entity, OWL.hasValue, Literal(int(character["score"]))))

        if character.get("height", None) is not None:
            g.add((entity, SDO.height, Literal(str(character["height"]))))
        if character.get("weight", None) is not None:
            g.add((entity, SDO.weight, Literal(str(character["weight"]))))
        if character.get("gender", None) is not None:
            g.add((entity, SDO.gender, Literal(character["gender"])))
        if character.get("place_of_birth", None) is not None:
            g.add((entity, SDO.birthPlace, Literal(character["place_of_birth"])))
        if character.get("full_name", None) is not None:
            g.add((entity, FOAF.name, Literal(character["full_name"])))
        if character.get("alignment", None) is not None:
            dbr = MARVEL_ALIGN_DBPEDIA.get(character["alignment"])
            if dbr is not None:
                g.add((entity, RDF.type, DBR[dbr]))

        for alias in character.get("aliases", []):
            g.add((entity, FOAF.nick, Literal(alias)))
        for race in character.get("races", []):
            r_node = EX["marv_race_" + format_name(race)]
            g.add((entity, RDF.type, r_node))
            dbr = MARVEL_RACES_DBPEDIA.get(race, None)

            g.add((r_node, RDFS.label, Literal(race)))
            g.add((r_node, RDFS.subClassOf, DBR["Race_(biology)"]))
            if dbr is not None:
                g.add((r_node, RDF.type, DBR[dbr]))

        for c in character.get("eye_color", []):
            g.add((entity, DBO.eyeColor, Literal(c)))
        for c in character.get("hair_color", []):
            g.add((entity, DBO.hairColor, Literal(c)))
        for occ in character.get("occupations", []):
            g.add((entity, SDO.hasOccupation, Literal(occ)))

        for work in character.get("stories", []):
            g.add((entity, DBO.participatingIn, Literal(work)))
        poke_types_ontology(g, character, entity)

    g.serialize(destination="data/ontology/marvel/final.ttl")
    return g


def marvel_get_json_ld(g, card_id, id_to_ld):
    if card_id is None:
        return None
    context = {
        "owl": "http://www.w3.org/2002/07/owl#", "sdo": "https://schema.org/",
        "dbr": "http://dbpedia.org/resource/", "poke": "https://triplydb.com/academy/pokemon/vocab/",
        "foaf": "http://xmlns.com/foaf/0.1/", "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "dbo": "http://dbpedia.org/ontology/"
    }
    marvel_ld = id_to_ld(g, card_id, context)
    marvel_ld["foaf:member"] = {**id_to_ld(g, marvel_ld["foaf:member"]["@id"], context)}
    marvel_ld["foaf:member"].pop("@context")

    for f in ["dbo:eyeColor", "dbo:hairColor", "dbo:participatingIn", "sdo:hasOccupation", "foaf:nick", "rdfs:seeAlso"]:
        if marvel_ld.get(f, None) is not None:
            marvel_ld[f] = to_list(marvel_ld[f])
    for p in ["poke:type"]:
        if marvel_ld.get(p, None) is not None:
            marvel_ld[p] = to_list(marvel_ld[p])

            for i in range(len(marvel_ld[p])):
                marvel_ld[p][i] = {**id_to_ld(g, marvel_ld[p][i]["@id"], context)}
                marvel_ld[p][i].pop("@context")

                if marvel_ld[p][i].get("dbo:defeat", None) is not None:
                    marvel_ld[p][i]["dbo:defeat"] = to_list(marvel_ld[p][i]["dbo:defeat"])

    for i in range(len(marvel_ld.get("@type", []))):
        if API_NAMESPACE in marvel_ld["@type"][i]:
            continue
            marvel_ld["@type"][i] = {**id_to_ld(g, marvel_ld["@type"][i], context)}
            marvel_ld["@type"][i].pop("@context")
    return marvel_ld


def marvel_get_json(json_ld):
    if json_ld is None:
        return None
    alignment = None
    races = []
    for t in json_ld.get("@type", []):
        if type(t) is dict:
            races.append(t["rdfs:label"])
            continue

        for k in MARVEL_ALIGN_DBPEDIA.keys():
            if t == "dbr:" + MARVEL_ALIGN_DBPEDIA[k]:
                alignment = k

    return dict_keys_filter({
        "universe": json_ld.get("foaf:member", {}).get("rdfs:label", None),
        "avatar": json_ld.get("foaf:img", {}).get("@id", None),
        "score": json_ld.get("owl:hasValue", 0),
        "name": json_ld.get("rdfs:label", None),
        "place_of_birth": json_ld.get("sdo:birthPlace", None),
        "height": json_ld.get("sdo:height", None),
        "weight": json_ld.get("sdo:weight", None),
        "gender": json_ld.get("sdo:gender", None),
        "alias": json_ld.get("foaf:nick", None),
        "full_name": json_ld.get("foaf:name", None),
        "occupations": json_ld.get("sdo:hasOccupation", None),
        "eye_color": json_ld.get("dbo:eyeColor", None),
        "hair_color": json_ld.get("dbo:hairColor", None),
        "stories": json_ld.get("dbo:participatingIn", None),
        "alignment": alignment,
        "race": races,
        "types": [{
            "name": b["rdfs:label"],
            "defeats": [d["@id"].replace(API_NAMESPACE + "type_", "") for d in b.get("dbo:defeat", [])]
        } for b in json_ld.get("poke:type", [])]
    }, filters=[None, [], {}])
