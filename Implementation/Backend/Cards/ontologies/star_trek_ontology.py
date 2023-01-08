from rdflib import URIRef, Literal, OWL, SSN, RDFS
from rdflib.namespace import FOAF, RDF, SDO, GEO, XSD

from tools.common_utils import *
from tools.ontology_macros import *
from tools.ontology_utils import query_dbpedia_by_keyword, format_name, poke_types_ontology


def star_trek_build_ontology(g, limit=None):
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

    all_species = load_json_file_to_dict("data/json/star_trek/final.json")
    universe = EX["univ_Star_Trek"]
    g.add((universe, RDFS.label, Literal("Star Trek")))
    g.add((universe, OWL.sameAs, DBR.Star_Trek))

    index = 0
    for species in all_species["species"]:
        index += 1
        if limit is not None and index > limit:
            break

        entity = EX["card_" + format_name(species["name"])]
        g.add((entity, FOAF.member, universe))
        dbr = query_dbpedia_by_keyword("star trek " + species["name"], species["name"])
        if dbr is not None:
            print(dbr)
            g.add((entity, RDFS.seeAlso, DBR[dbr]))

        g.add((entity, RDF.type, DBR.Playing_card))
        g.add((entity, RDF.type, DBC.Lists_of_fictional_species))
        g.add((entity, RDF.type, DBC.Star_Trek_species))

        g.add((entity, RDFS.label, Literal(species["name"])))
        g.add((entity, FOAF.img, URIRef(species["avatar"])))
        g.add((entity, OWL.hasValue, Literal(int(species["score"]))))

        planet, quadrant = None, None
        if species.get("quadrant", None) is not None:
            quadrant = EX["trek_quad_" + format_name(species["quadrant"])]
        if species.get("homeworld", None) is not None:
            planet = EX["trek_plan_" + format_name(species["homeworld"])]
        if planet is not None and "quadrant" in str(planet).lower():
            planet = None

        if planet is not None:
            g.add((planet, RDF.type, DBC.Fictional_planets))
            g.add((planet, RDFS.label, Literal(species["homeworld"])))
            g.add((entity, SDO.birthPlace, planet))

            if quadrant is not None:
                g.add((planet, GEO.ehInside, quadrant))

        if quadrant is not None:
            g.add((quadrant, RDF.type, DBR.Galactic_quadrant))
            g.add((quadrant, RDFS.label, Literal(species["quadrant"])))
            g.add((entity, SDO.birthPlace, quadrant))

            if planet is not None:
                g.add((quadrant, GEO.ehContains, planet))

        poke_types_ontology(g, species, entity)
        for power in [a for a in species.keys() if "Species" in a or "alternate" in a]:
            dbr = STAR_TREK_PROP_DBPEDIA.get(power, None)
            power_node = EX["trek_prop_" + power]

            if dbr is not None:
                g.add((power_node, OWL.sameAs, DBR[dbr]))
            g.add((power_node, RDFS.label, Literal(power)))
            g.add((entity, SSN.hasProperty, power_node))

    g.serialize(destination="data/ontology/star_trek/final.ttl")
    return g


def star_trek_get_json_ld(g, card_id, id_to_ld):
    if card_id is None:
        return None
    context = {
        "owl": "http://www.w3.org/2002/07/owl#", "sdo": "https://schema.org/",
        "dbr": "http://dbpedia.org/resource/", "poke": "https://triplydb.com/academy/pokemon/vocab/",
        "foaf": "http://xmlns.com/foaf/0.1/", "ssn": "http://www.w3.org/ns/ssn/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#", "geo": "http://www.opengis.net/ont/geosparql#",
        "dbo": "http://dbpedia.org/ontology/"
    }
    star_trek_ld = id_to_ld(g, card_id, context)
    star_trek_ld["foaf:member"] = {**id_to_ld(g, star_trek_ld["foaf:member"]["@id"], context)}
    star_trek_ld["foaf:member"].pop("@context")

    if star_trek_ld.get('sdo:birthPlace', None) is not None:
        star_trek_ld['sdo:birthPlace'] = to_list(star_trek_ld['sdo:birthPlace'])

        for i in range(len(star_trek_ld['sdo:birthPlace'])):
            star_trek_ld['sdo:birthPlace'][i] = {**id_to_ld(g, star_trek_ld['sdo:birthPlace'][i]["@id"], context)}
            star_trek_ld['sdo:birthPlace'][i].pop("@context")
            star_trek_ld['sdo:birthPlace'][i].pop('geo:ehInside', None)
            star_trek_ld['sdo:birthPlace'][i].pop('geo:ehContains', None)

    for p in ["rdfs:seeAlso"]:
        if star_trek_ld.get(p, None) is not None:
            star_trek_ld[p] = to_list(star_trek_ld[p])
    for p in ["poke:type", "ssn:hasProperty"]:
        if star_trek_ld.get(p, None) is not None:
            star_trek_ld[p] = to_list(star_trek_ld[p])

            for i in range(len(star_trek_ld[p])):
                star_trek_ld[p][i] = {**id_to_ld(g, star_trek_ld[p][i]["@id"], context)}
                star_trek_ld[p][i].pop("@context")

                if star_trek_ld[p][i].get("dbo:defeat", None) is not None:
                    star_trek_ld[p][i]["dbo:defeat"] = to_list(star_trek_ld[p][i]["dbo:defeat"])

    star_trek_ld["@context"].pop("geo")
    return star_trek_ld


def star_trek_get_json(json_ld):
    if json_ld is None:
        return None
    return dict_keys_filter({
        "universe": json_ld.get("foaf:member", {}).get("rdfs:label", None),
        "avatar": json_ld.get("foaf:img", {}).get("@id", None),
        "score": json_ld.get("owl:hasValue", 0),
        "name": json_ld.get("rdfs:label", None),
        "homeworld": get_first_element_list(
            [b["rdfs:label"] for b in json_ld.get("sdo:birthPlace", []) if "trek_plan_" in b["@id"]]
        ),
        "quadrant": get_first_element_list(
            [b["rdfs:label"] for b in json_ld.get("sdo:birthPlace", []) if "trek_quad_" in b["@id"]]
        ),
        "species": [s["rdfs:label"] for s in json_ld.get("ssn:hasProperty", [])],
        "types": [{
            "name": b["rdfs:label"],
            "defeats": [d["@id"].replace(API_NAMESPACE + "type_", "") for d in b.get("dbo:defeat", [])]
        } for b in json_ld.get("poke:type", [])]
    }, filters=[None, []])
