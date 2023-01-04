from rdflib import URIRef, Literal, OWL, SSN, RDFS
from rdflib.namespace import FOAF, RDF, SDO, GEO, XSD

from tools.common_utils import *
from tools.ontology_macros import *
from tools.ontology_utils import format_name, query_dbpedia_by_keyword, poke_types_ontology


def star_wars_build_ontology(g, limit=None):
    g.bind("dbr", DBR)
    g.bind("ex", EX)
    g.bind("foaf", FOAF)
    g.bind("geo", GEO)
    g.bind("owl", OWL)
    g.bind("poke", POKE)
    g.bind("rdfs", RDFS)
    g.bind("sdo", SDO)
    g.bind("ssn", SSN)
    g.bind("xsd", XSD)
    g.bind("swapi", SWAPI)

    all_people = load_json_file_to_dict("data/json/star_wars/final.json")
    universe = EX["univ_Star_Wars"]
    g.add((universe, RDFS.label, Literal("Star Wars")))
    g.add((universe, OWL.sameAs, DBR.Star_Wars))

    index = 0
    for person in all_people["people"]:
        index += 1
        if limit is not None and index > limit:
            break

        entity = EX["card_" + format_name(person["name"])]
        g.add((entity, FOAF.member, universe))
        dbr = query_dbpedia_by_keyword("star wars " + person["name"], person["name"])
        if dbr is not None:
            print(dbr)
            g.add((entity, RDFS.seeAlso, DBR[dbr]))

        g.add((entity, RDF.type, DBR.Playing_card))
        g.add((entity, RDF.type, DBC.Lists_of_fictional_characters))
        g.add((entity, RDF.type, DBC.List_of_Star_Wars_characters))

        g.add((entity, RDFS.label, Literal(person["name"])))
        g.add((entity, FOAF.img, URIRef(person["avatar"])))
        g.add((entity, OWL.hasValue, Literal(int(person["score"]))))

        if person.get("birth_year", None) is not None:
            g.add((entity, SWAPI.birthYear, Literal(person["birth_year"])))
        if person.get("gender", None) is not None:
            g.add((entity, SWAPI.gender, Literal(person["gender"])))
        if person.get("mass", None) is not None:
            g.add((entity, SWAPI.mass, Literal(person["mass"])))
        if person.get("height", None) is not None:
            g.add((entity, SWAPI.height, Literal(person["height"])))

        for color in person.get("eye_color", []):
            g.add((entity, SWAPI.eyeColor, Literal(color)))
        for color in person.get("hair_color", []):
            g.add((entity, SWAPI.hairColor, Literal(color)))
        for color in person.get("skin_color", []):
            g.add((entity, SWAPI.skinColor, Literal(color)))

        for film in person.get("films", []):
            swapi_film = EX["wars_film_" + format_name(film["title"])]
            g.add((entity, SWAPI.film, swapi_film))

            g.add((swapi_film, RDFS.label, Literal(film["title"])))
            g.add((swapi_film, RDFS.seeAlso, DBR[STAR_WARS_FILM_DBPEDIA[film["title"]]]))
            g.add((swapi_film, SWAPI.director, Literal(film["director"])))
            g.add((swapi_film, SWAPI.releaseDate, Literal(film["release_date"])))
            for producer in film["producers"]:
                g.add((swapi_film, SWAPI.producer, Literal(producer)))

        if person.get("homeworld", None) is not None:
            planet = EX["wars_plan_" + format_name(person["homeworld"]["name"])]
            g.add((entity, SWAPI.homeworld, planet))

            g.add((planet, RDFS.label, Literal(person["homeworld"]["name"])))
            g.add((planet, RDF.type, SWAPI.Planet))
            if person["homeworld"].get("surface_water", None) is not None:
                g.add((planet, SWAPI.surfaceWater, Literal(person["homeworld"]["surface_water"])))
            for weather in person["homeworld"].get("climate", []):
                g.add((planet, SWAPI.climate, Literal(weather)))
            for t in person["homeworld"].get("terrain", []):
                g.add((planet, SWAPI.terrain, Literal(t)))

        for species in person.get("species", []):
            s_node = EX["wars_spec_" + format_name(species["name"])]
            g.add((entity, RDF.type, s_node))

            g.add((s_node, OWL.sameAs, SWAPI[format_name(species["name"])]))
            g.add((s_node, RDF.type, SWAPI.Species))
            g.add((s_node, RDFS.label, Literal(species["name"])))
            if species.get("average_lifespan", None) is not None:
                g.add((s_node, SWAPI.averageLifespan, Literal(species["average_lifespan"])))
            if species.get("classification", None) is not None:
                g.add((s_node, RDFS.subClassOf, Literal(species["classification"])))

        for o_name, o_predicate, o_type, o_lit in [
            ("starships", SWAPI.starship, SWAPI.Starship, "wars_ship_"),
            ("vehicles", SWAPI.vehicle, SWAPI.Vehicle, "wars_auto_")
        ]:
            for o in person.get(o_name, []):
                st_node = EX[o_lit + format_name(o["name"])]
                g.add((entity, o_predicate, st_node))

                g.add((st_node, RDF.type, o_type))
                g.add((st_node, RDFS.label, Literal(o["name"])))
                if o.get("crew", None) is not None:
                    g.add((st_node, SWAPI.crew, Literal(o["crew"])))
                if o.get("passengers", None) is not None:
                    g.add((st_node, SWAPI.passengers, Literal(o["passengers"])))
                if o.get("length", None) is not None:
                    g.add((st_node, SWAPI.length, Literal(o["length"])))
                if o.get("hyperdrive_rating", None) is not None:
                    g.add((st_node, SWAPI.hyperdriveRating, Literal(o["hyperdrive_rating"])))
                if o.get("max_atmosphering_speed", None) is not None:
                    g.add((st_node, SWAPI.maxAtmospheringSpeed, Literal(o["max_atmosphering_speed"])))

        poke_types_ontology(g, person, entity)

    g.serialize(destination="data/ontology/star_wars/final.ttl")
    return g


def star_wars_get_json_ld(g, card_id, id_to_ld):
    if card_id is None:
        return None
    context = {
        "owl": "http://www.w3.org/2002/07/owl#", "dbr": "http://dbpedia.org/resource/",
        "poke": "https://triplydb.com/academy/pokemon/vocab/", "foaf": "http://xmlns.com/foaf/0.1/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#", "swapi": "https://swapi.co/vocabulary/",
        "dbo": "http://dbpedia.org/ontology/"
    }
    star_wars_ld = id_to_ld(g, card_id, context)
    star_wars_ld["foaf:member"] = {**id_to_ld(g, star_wars_ld["foaf:member"]["@id"], context)}
    star_wars_ld["foaf:member"].pop("@context")

    if star_wars_ld.get('swapi:homeworld', None) is not None:
        star_wars_ld['swapi:homeworld'] = {**id_to_ld(g, star_wars_ld['swapi:homeworld']["@id"], context)}
        for p in ["swapi:climate", "swapi:terrain"]:
            if star_wars_ld['swapi:homeworld'].get(p, None) is not None:
                star_wars_ld['swapi:homeworld'][p] = to_list(star_wars_ld['swapi:homeworld'][p])
        star_wars_ld['swapi:homeworld'].pop("@context")

    for p in ["swapi:eyeColor", "swapi:hairColor", "swapi:skinColor"]:
        if star_wars_ld.get(p, None) is not None:
            star_wars_ld[p] = to_list(star_wars_ld[p])

    for p in ["swapi:starship", "swapi:vehicle", "poke:type", "swapi:film"]:
        if star_wars_ld.get(p, None) is not None:
            star_wars_ld[p] = to_list(star_wars_ld[p])

            for i in range(len(star_wars_ld[p])):
                star_wars_ld[p][i] = {**id_to_ld(g, star_wars_ld[p][i]["@id"], context)}
                star_wars_ld[p][i].pop("@context")

                if star_wars_ld[p][i].get('swapi:producer', None) is not None:
                    star_wars_ld[p][i]['swapi:producer'] = to_list(star_wars_ld[p][i]['swapi:producer'])
                if star_wars_ld[p][i].get("dbo:defeat", None) is not None:
                    star_wars_ld[p][i]["dbo:defeat"] = to_list(star_wars_ld[p][i]["dbo:defeat"])

    for i in range(len(star_wars_ld.get("@type", []))):
        if API_NAMESPACE in star_wars_ld["@type"][i]:
            star_wars_ld["@type"][i] = {**id_to_ld(g, star_wars_ld["@type"][i], context)}
            star_wars_ld["@type"][i].pop("@context")
    return star_wars_ld


def star_wars_get_json(json_ld):
    if json_ld is None:
        return None
    species_list = []
    for s in json_ld.get("@type", []):
        if type(s) is not dict:
            continue
        if API_NAMESPACE in s.get("@id", ""):
            species_list.append(dict_keys_filter({
                "name": s.get("rdfs:label", None),
                "average_lifespan": s.get("swapi:averageLifespan", None),
                "classification": s.get("rdfs:subClassOf", None)
            }))

    return dict_keys_filter({
        "universe": json_ld.get("foaf:member", {}).get("rdfs:label", None),
        "avatar": json_ld.get("foaf:img", {}).get("@id", None),
        "score": json_ld.get("owl:hasValue", 0),
        "name": json_ld.get("rdfs:label", None),
        "height": json_ld.get("swapi:height", None),
        "weight": json_ld.get("swapi:mass", None),
        "gender": json_ld.get("swapi:gender", None),
        "birth_year": json_ld.get("swapi:birthYear", None),
        "skin_color": json_ld.get("swapi:skinColor", None),
        "hair_color": json_ld.get("swapi:hairColor", None),
        "eye_color": json_ld.get("swapi:eyeColor", None),
        "homeworld": dict_keys_filter({
            "name": json_ld.get("swapi:homeworld", {}).get("rdfs:label", None),
            "climate": json_ld.get("swapi:homeworld", {}).get("swapi:climate", None),
            "surfaceWater": json_ld.get("swapi:homeworld", {}).get("swapi:surfaceWater", None),
            "terrain": json_ld.get("swapi:homeworld", {}).get("swapi:terrain", None)
        }),
        "films": [dict_keys_filter({
            "title": film.get("rdfs:label", None),
            "director": film.get("swapi:director", None),
            "producers": film.get("swapi:producer", None),
            "release_date": film.get("swapi:releaseDate", None)
        }) for film in json_ld.get("swapi:film", [])],
        "starships": [dict_keys_filter({
            "name": ship.get("rdfs:label", None),
            "crew": ship.get("swapi:crew", None),
            "hyperdrive_rating": ship.get("swapi:hyperdriveRating", None),
            "length": ship.get("swapi:length", None),
            "max_atmosphering_speed": ship.get("swapi:maxAtmospheringSpeed", None),
            "passengers": ship.get("swapi:passengers", None)
        }) for ship in json_ld.get("swapi:starship", [])],
        "vehicles": [dict_keys_filter({
            "name": vehicle.get("rdfs:label", None),
            "crew": vehicle.get("swapi:crew", None),
            "hyperdrive_rating": vehicle.get("swapi:hyperdriveRating", None),
            "length": vehicle.get("swapi:length", None),
            "max_atmosphering_speed": vehicle.get("swapi:maxAtmospheringSpeed", None),
            "passengers": vehicle.get("swapi:passengers", None)
        }) for vehicle in json_ld.get("swapi:vehicle", [])],
        "species": species_list,
        "types": [{
            "name": b["rdfs:label"],
            "defeats": [d["@id"].replace(API_NAMESPACE + "type_", "") for d in b.get("dbo:defeat", [])]
        } for b in json_ld.get("poke:type", [])]
    }, filters=[None, [], {}])
