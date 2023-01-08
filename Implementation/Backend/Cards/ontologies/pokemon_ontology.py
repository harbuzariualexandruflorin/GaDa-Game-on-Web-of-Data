import random

from rdflib import URIRef, Literal, OWL, RDFS, SDO
from rdflib.namespace import FOAF, RDF, XSD

from tools.common_utils import *
from tools.ontology_macros import *
from tools.ontology_utils import format_name, poke_types_ontology, query_dbpedia_by_keyword


def randomise_pokemon(all_pokemon, n_chunks, target_nr):
    all_pokemon = sorted(all_pokemon, key=lambda p: p["score"])
    best_pokemon = all_pokemon[len(all_pokemon) - 50:]
    chunk_size = len(all_pokemon) // n_chunks
    random_pokemon = []
    chunks = {}

    for chunk in range(0, n_chunks):
        if chunk == n_chunks - 1:
            chunks[chunk] = all_pokemon[chunk * chunk_size:]
        else:
            chunks[chunk] = all_pokemon[chunk * chunk_size:(chunk + 1) * chunk_size]

    while len(random_pokemon) < target_nr:
        for chunk in range(0, n_chunks):
            random_pokemon.append(chunks[chunk].pop(random.randrange(len(chunks[chunk]))))

    to_add = []
    for best in best_pokemon:
        found = False
        for r in random_pokemon:
            if r["name"] == best["name"]:
                found = True
                break
        if found is not True:
            to_add.append(best)
    return random_pokemon + to_add


def pokemon_build_ontology(g, limit=None):
    all_pokemon = load_json_file_to_dict("data/json/pokemon/final.json")
    all_pokemon["pokemon"] = randomise_pokemon(all_pokemon["pokemon"], 10, 200)
    all_pokemon["pokemon"] = sorted(all_pokemon["pokemon"], key=lambda p: p["score"])

    g.bind("dbr", DBR)
    g.bind(PREFIX_EX, EX)
    g.bind("foaf", FOAF)
    g.bind("owl", OWL)
    g.bind("poke", POKE)
    g.bind("rdfs", RDFS)
    g.bind("sdo", SDO)
    g.bind("xsd", XSD)

    universe = EX["univ_Pokemon"]
    g.add((universe, RDFS.label, Literal("Pokemon")))
    g.add((universe, OWL.sameAs, DBR.Pokémon))

    index = 0
    for pokemon in all_pokemon["pokemon"]:
        index += 1
        if limit is not None and index > limit:
            break

        entity = EX["card_" + format_name(pokemon["name"])]
        g.add((entity, FOAF.member, universe))
        dbr = query_dbpedia_by_keyword("pokémon " + pokemon["species"], pokemon["species"])
        if dbr is not None:
            print(dbr)
            g.add((entity, RDFS.seeAlso, DBR[dbr]))

        g.add((entity, RDF.type, DBR.Playing_card))
        g.add((entity, RDF.type, POKE.Pokémon))
        g.add((entity, RDF.type, DBC.Lists_of_fictional_characters))
        g.add((entity, RDFS.seeAlso, DBC.Pokémon_species))

        g.add((entity, RDFS.label, Literal(pokemon["name"])))
        g.add((entity, FOAF.img, URIRef(pokemon["avatar"])))
        g.add((entity, OWL.hasValue, Literal(int(pokemon["score"]))))

        if pokemon.get("color", None) is not None:
            g.add((entity, POKE.colour, Literal(pokemon["color"])))
        if pokemon.get("experience", None) is not None:
            g.add((entity, POKE.baseExp, Literal(pokemon["experience"])))
        if pokemon.get("height", None) is not None:
            g.add((entity, SDO.height, Literal(str(pokemon["height"]))))
        if pokemon.get("weight", None) is not None:
            g.add((entity, POKE.weight, Literal(str(pokemon["weight"]))))
        if pokemon.get("species", None) is not None:
            g.add((entity, POKE.species, Literal(pokemon["species"])))

        for ab in pokemon.get("abilities", []):
            g.add((entity, POKE.ability, Literal(ab)))
        if pokemon.get("stats", None) is not None:
            if pokemon["stats"].get("hp", None) is not None:
                g.add((entity, POKE.baseHP, Literal(pokemon["stats"]["hp"])))
            if pokemon["stats"].get("attack", None) is not None:
                g.add((entity, POKE.baseAttack, Literal(pokemon["stats"]["attack"])))
            if pokemon["stats"].get("defense", None) is not None:
                g.add((entity, POKE.baseDefense, Literal(pokemon["stats"]["defense"])))
            if pokemon["stats"].get("special_attack", None) is not None:
                g.add((entity, POKE.baseSpAtk, Literal(pokemon["stats"]["special_attack"])))
            if pokemon["stats"].get("special_defense", None) is not None:
                g.add((entity, POKE.baseSpDef, Literal(pokemon["stats"]["special_defense"])))
            if pokemon["stats"].get("speed", None) is not None:
                g.add((entity, POKE.baseSpeed, Literal(pokemon["stats"]["speed"])))

        poke_types_ontology(g, pokemon, entity)

    g.serialize(destination="data/ontology/pokemon/final.ttl")
    return g


def pokemon_get_json_ld(g, card_id, id_to_ld):
    if card_id is None:
        return None
    context = {
        "owl": "http://www.w3.org/2002/07/owl#", "sdo": "https://schema.org/",
        "dbr": "http://dbpedia.org/resource/", "poke": "https://triplydb.com/academy/pokemon/vocab/",
        "foaf": "http://xmlns.com/foaf/0.1/", "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "dbo": "http://dbpedia.org/ontology/"
    }
    pokemon_ld = id_to_ld(g, card_id, context)
    pokemon_ld["foaf:member"] = {**id_to_ld(g, pokemon_ld["foaf:member"]["@id"], context)}
    pokemon_ld["foaf:member"].pop("@context")

    if pokemon_ld.get('poke:ability', None) is not None:
        pokemon_ld['poke:ability'] = to_list(pokemon_ld['poke:ability'])
    for p in ["poke:type"]:
        if pokemon_ld.get(p, None) is not None:
            pokemon_ld[p] = to_list(pokemon_ld[p])

            for i in range(len(pokemon_ld[p])):
                pokemon_ld[p][i] = {**id_to_ld(g, pokemon_ld[p][i]["@id"], context)}
                pokemon_ld[p][i].pop("@context")

                if pokemon_ld[p][i].get("dbo:defeat", None) is not None:
                    pokemon_ld[p][i]["dbo:defeat"] = to_list(pokemon_ld[p][i]["dbo:defeat"])
    return pokemon_ld


def pokemon_get_json(json_ld):
    if json_ld is None:
        return None

    return dict_keys_filter({
        "universe": json_ld.get("foaf:member", {}).get("rdfs:label", None),
        "avatar": json_ld.get("foaf:img", {}).get("@id", None),
        "score": json_ld.get("owl:hasValue", 0),
        "name": json_ld.get("rdfs:label", None),
        "color": json_ld.get("poke:colour", None),
        "abilities": json_ld.get("poke:ability", None),
        "species": json_ld.get("poke:species", None),
        "weight": json_ld.get("poke:weight", None),
        "height": json_ld.get("sdo:height", None),
        "experience": json_ld.get("poke:baseExp", None),
        "stats": dict_keys_filter({
            "attack": json_ld.get("poke:baseAttack", None),
            "defense": json_ld.get("poke:baseDefense", None),
            "hp": json_ld.get("poke:baseHP", None),
            "special_attack": json_ld.get("poke:baseSpAtk", None),
            "special_defense": json_ld.get("poke:baseSpDef", None),
            "speed": json_ld.get("poke:baseSpeed", None),
        }),
        "types": [{
            "name": b["rdfs:label"],
            "defeats": [d["@id"].replace(API_NAMESPACE + "type_", "") for d in b.get("dbo:defeat", [])]
        } for b in json_ld.get("poke:type", [])]
    }, filters=[None, [], {}])
