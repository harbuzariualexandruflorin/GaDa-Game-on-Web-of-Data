from http import HTTPStatus

import requests

from tools import *


def pokemon_get_species_api(url):
    try:
        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            print("ERROR STATUS CODE NOT OK IN api call " + url)
            return dict()
        species_json = json.loads(response.content.decode())
    except:
        print("ERROR IN api call " + url)
        return dict()
    return {
        "color": species_json.get("color", {}).get("name", None)
    }


def pokemon_get_pokemon_api(url):
    try:
        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            print("ERROR STATUS CODE NOT OK IN api call " + url)
            return dict()
        pokemon_json = json.loads(response.content.decode())
    except:
        print("ERROR IN api call " + url)
        return dict()

    stats = {}
    for stat in pokemon_json.get("stats", []):
        if stat.get("stat", {}).get("name", None) is None:
            continue
        stats[stat["stat"]["name"].replace("-", "_")] = stat.get("base_stat", 0)

    types = []
    for p_type in pokemon_json.get("types", []):
        if p_type.get("type", {}).get("name", None) is not None:
            types.append(p_type["type"]["name"])
    if len(types) == 0:
        types = None

    avatar = pokemon_json.get("sprites", {}).get("other", {}).get("official-artwork", {}).get("front_default", None)
    if avatar is None:
        avatar = pokemon_json.get("sprites", {}).get("front_default", None)
    if avatar is None:
        avatar = pokemon_json.get("sprites", {}).get("other", {}).get("home", {}).get("front_default", None)
    if avatar is None:
        raise Exception("Skipping pokemon... No avatar found for pokemon " + url)

    abilities = []
    for a in pokemon_json.get("abilities", []):
        if a.get("ability", {}).get("name", None) is not None:
            abilities.append(a["ability"]["name"])
    abilities = list(dict.fromkeys(abilities))
    if len(abilities) == 0:
        abilities = None

    return dict_keys_filter({
        "universe": "Pokemon",
        "id": "pokemon:" + str(pokemon_json["id"]),
        "nr_abilities": len(pokemon_json.get("abilities", [])),
        "abilities": abilities,
        "experience": pokemon_json.get("base_experience", 0),
        "nr_forms": len(pokemon_json.get("forms", [])),
        "height": pokemon_json.get("height", 0),
        "nr_moves": len(pokemon_json.get("moves", [])),
        "species": pokemon_json.get("species", {}).get("name", None),
        **pokemon_get_species_api(pokemon_json.get("species", {}).get("url", None)),
        "avatar": avatar,
        "stats": stats,
        "types": types,
        "weight": pokemon_json.get("weight", 0),
    })


def pokemon_get_entities_api(url='https://pokeapi.co/api/v2/pokemon?limit=9999&offset=0'):
    all_pokemon = {"pokemon": []}
    current_ids = []
    try:
        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            return all_pokemon
        pokemon_json = json.loads(response.content.decode())
    except:
        return all_pokemon

    index = 0
    for pokemon in pokemon_json["results"]:
        index += 1
        print("Pokemon " + str(index), " done!")

        try:
            if pokemon.get("name", None) is None or pokemon.get("url", None) is None:
                print("Skipping pokemon... No name/id found for pokemon " + str(pokemon))
                continue
            if pokemon["url"] in current_ids:
                print("Skipping pokemon... Duplicate id found for pokemon " + str(pokemon))
                continue

            pokemon_dict = pokemon_get_pokemon_api(pokemon["url"])
            if len(pokemon_dict.keys()) > 0:
                current_ids.append(pokemon["url"])
                all_pokemon["pokemon"].append({
                    "name": pokemon["name"], **pokemon_dict
                })
        except Exception as ex:
            print("POKEMON API SCRAPER EXCEPTION: ", ex)
    return all_pokemon


def pokemon_get_score(all_pokemon):
    return entities_get_score(POKEMON_VARS, all_pokemon)


def pokemon_build_json():
    return
    # entities = pokemon_get_entities_api()
    # save_dict_to_json_file(entities, "data/json/pokemon/api_orig.json")
    # entities = load_json_file_to_dict("data/json/pokemon/api_orig.json")
    # scores = pokemon_get_score(entities)
    # check_range_score(scores)
    # save_dict_to_json_file(scores, "data/json/pokemon/final.json")
