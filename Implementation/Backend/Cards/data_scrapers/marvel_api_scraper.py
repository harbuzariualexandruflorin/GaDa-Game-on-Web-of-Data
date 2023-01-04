from http import HTTPStatus

import requests
from marvel import Marvel

from tools import *


def marvel_get_entities_api():
    marvel_api = Marvel(MARVEL_API_KEYS["public"], MARVEL_API_KEYS["private"])
    all_characters = {"characters": []}
    off = 0

    while True:
        characters = marvel_api.characters.all(offset=off, limit=100)
        print("Offset Marvel " + str(off) + " done!")
        if characters["data"]["count"] == 0:
            break
        off += characters["data"]["count"]
        all_characters["characters"] += characters["data"]["results"]
    return all_characters


def marvel_process_collection(character, collection_key, condition=None):
    if condition is None:
        condition = lambda x: True
    collection = []

    for c in character[collection_key]["items"]:
        if condition(c):
            collection.append(c["name"])
    if len(collection) == 0:
        collection = None
    return collection


def marvel_process_entity(character):
    if "image_not_available" in character["thumbnail"]["path"]:
        return dict()
    if "gif" in character["thumbnail"]["extension"]:
        return dict()

    comics = marvel_process_collection(character, "comics")
    series = marvel_process_collection(character, "series")
    events = marvel_process_collection(character, "events")
    stories = marvel_process_collection(
        character, "stories",
        lambda x: x["type"] == "cover" and len([s for s in [" of ", "cover", "variant"] if s in x["name"].lower()]) == 0
    )

    return dict_keys_filter({
        "id": "marvel:" + str(character["id"]),
        "name": character["name"],
        "avatar": character["thumbnail"]["path"] + "." + character["thumbnail"]["extension"],
        "nr_comics": 0 if comics is None else len(comics),
        "comics": comics,
        "nr_series": 0 if series is None else len(series),
        "series": series,
        "nr_stories": 0 if stories is None else len(stories),
        "stories": stories,
        "nr_events": 0 if events is None else len(events),
        "events": events
    })


def marvel_process_entities(all_characters):
    new_characters = {"characters": []}
    current_ids = []

    for character in all_characters["characters"]:
        if character.get("name", None) is None or character.get("id", None) is None:
            print("Skipping character... No name/id found for character " + str(character))
            continue
        if character["id"] in current_ids:
            print("Skipping character... Duplicate id found for character " + str(character))
            continue

        new_character = marvel_process_entity(character)
        if len(new_character.keys()) > 0:
            current_ids.append(character["id"])
            new_characters["characters"].append(new_character)
    return new_characters


def marvel_stats_dict(stats_json):
    aliases = []
    for alias in [a.split("(")[0].strip() for a in stats_json["biography"]["aliases"]]:
        s = split_by_char(alias, "[;,]")
        if s is None:
            continue
        for a in s:
            if "also" in a.lower():
                s = []
                break
        aliases += s
    if len(aliases) == 0 or "-" in aliases:
        aliases = None

    stats = dict_keys_filter({**stats_json["powerstats"]}, [None, "null"])
    if len(stats.KEYS()) == 0:
        return None

    birth_place = stats_json["biography"]["place-of-birth"]
    if "Montreal" in birth_place:
        birth_place = "Montreal, Quebec, Canada"
    temp = birth_place.lower()
    for c in ["unrevealed", "undisclosed", "unknown", ";", "unnamed", "somewhere", "presumably", "unidentified"]:
        if c in temp:
            birth_place = None

    races = split_by_char(stats_json["appearance"]["race"], "/")
    if len(races) == 0 or "null" in races:
        races = None

    height = get_first_element_list([h for h in stats_json["appearance"]["height"] if "cm" in h])
    if height is not None:
        height = height.split()[0]
    weight = get_first_element_list([w for w in stats_json["appearance"]["weight"] if "kg" in w])
    if weight is not None:
        weight = weight.split()[0]

    eye_color = [e.split("(")[0].strip() for e in split_by_char(stats_json["appearance"]["eye-color"], "/")]
    if len(eye_color) == 0 or "null" in eye_color or "-" in eye_color:
        eye_color = None
    hair_color = split_by_char(stats_json["appearance"]["hair-color"], "/")
    if len(hair_color) == 0 or "null" in hair_color or "-" in hair_color or 'no hair' in [h.lower() for h in hair_color]:
        hair_color = None

    occupations = []
    for o in split_by_char(stats_json["work"]["occupation"], "[;,]"):
        o = o.split("(")[0].strip()
        if "prostitute" in o.lower():
            return None
        if "unknown" in o.lower():
            continue
        if ")" in o and "(" not in o:
            continue
        if len(o) > 0:
            occupations.append(o)
    if len(occupations) == 0 or "-" in occupations:
        occupations = None
    if "usually" in stats_json["work"]["occupation"] or "was" in stats_json["work"]["occupation"]:
        occupations = None
    if "California" in stats_json["work"]["occupation"]:
        occupations = None
    if "representing" in stats_json["work"]["occupation"]:
        occupations = None

    return dict_keys_filter({
        "stats": stats,
        "full_name": stats_json["biography"]["full-name"].split("(")[0].strip(),
        "aliases": aliases,
        "nr_aliases": 0 if aliases is None else len(aliases),
        "place_of_birth": birth_place,
        "alignment": stats_json["biography"]["alignment"],
        "gender": stats_json["appearance"]["gender"],
        "races": races,
        "height": None if height in ["0", None] else height,
        "weight": None if weight in ["0", None] else weight,
        "eye_color": eye_color,
        "hair_color": hair_color,
        "occupations": occupations
    }, [None, "", "-", "n/a"])


def marvel_stats_entity(current_ids, character, url="https://www.superheroapi.com/api.php/%s/search/%s"):
    try:
        response = requests.get(url % (SUPERHERO_API_KEY, character["name"]))
        if response.status_code != HTTPStatus.OK:
            print("ERROR STATUS CODE NOT OK IN api call " + url)
            return None
        superhero_json = json.loads(response.content.decode())
    except:
        print("ERROR IN api call " + url)
        return None

    if superhero_json["response"] == "error":
        return None
    if superhero_json["results-for"] in current_ids:
        print("Skipping marvel hero... Duplicate found for " + str(character))
        return None
    current_ids.append(superhero_json["results-for"])
    return marvel_stats_dict(superhero_json["results"][0])


def marvel_get_stats(all_characters):
    new_characters = {"characters": []}
    current_ids = []

    for character in all_characters["characters"]:
        new_character = marvel_stats_entity(current_ids, character)
        if new_character is not None:
            print({**character, **new_character})
            new_characters["characters"].append({**character, **new_character})
    return new_characters


def marvel_get_types(all_characters):
    for character in all_characters["characters"]:
        types = []
        if int(character["stats"].get("speed", 0)) == 100:
            types.append(CARD_TYPES.teleport)
        for s in ["strength", "power", "combat"]:
            if int(character["stats"].get(s, 0)) > 80:
                types.append(CARD_TYPES.fighting)
                break

        for a in character.get("aliases", []):
            if "witch" in a.lower() or "sorcerer" in a.lower():
                types += [CARD_TYPES.fairy, CARD_TYPES.psychic, CARD_TYPES.teleport, CARD_TYPES.flying]
                break

        for o in character.get("occupations", []):
            if "mutant leader" in o.lower():
                types += [CARD_TYPES.psychic]
                break
            for t in ["soldier", "mercenary", "wrestler", "fighter", "warrior", "conqueror"]:
                if t in o.lower():
                    types += [CARD_TYPES.fighting]
                    break
            for t in ["sorceress", "sorcerer"]:
                if t in o.lower():
                    types += [CARD_TYPES.fairy, CARD_TYPES.flying, CARD_TYPES.psychic, CARD_TYPES.teleport]
                    break
            if "dark" in o.lower():
                types += [CARD_TYPES.dark]
            if "nuclear" in o.lower():
                types += [CARD_TYPES.poison]
            if "hell" in o.lower():
                types += [CARD_TYPES.fire, CARD_TYPES.dark]
            if "God" in o:
                types += MARVEL_TYPES["God"]
            for t in ["death", "galactus"]:
                if t in o.lower():
                    types += [CARD_TYPES.dark, CARD_TYPES.poison]
                    break

        entity = {}
        for r in character.get("races", []):
            entity[r] = True
        temp = get_entity_types(MARVEL_TYPES, entity)
        if temp is None:
            temp = []

        types = [t.name for t in types]
        types += temp
        types = list(dict.fromkeys(types))

        if len(types) > 0:
            character["types"] = types
    return all_characters


def marvel_get_score(all_characters):
    temp = marvel_get_types(all_characters)
    all_characters = {"characters": [c for c in temp["characters"] if ".gif" not in c["avatar"]]}
    for character in all_characters["characters"]:
        character["universe"] = "Marvel"
    return entities_get_score(MARVEL_VARS, all_characters)


def marvel_build_json():
    return
    # entities = marvel_get_entities_api()
    # save_dict_to_json_file(entities, "data/json/marvel/api_orig.json")

    # entities = load_json_file_to_dict("data/json/marvel/api_orig.json")
    # entities = marvel_process_entities(entities)
    # save_dict_to_json_file(entities, "data/json/marvel/orig_processed.json")

    # entities = load_json_file_to_dict("data/json/marvel/orig_processed.json")
    # entities = marvel_get_stats(entities)
    # save_dict_to_json_file(entities, "data/json/marvel/processed_stats.json")

    # entities = load_json_file_to_dict("data/json/marvel/processed_stats.json")
    # scores = marvel_get_score(entities)
    # check_range_score(scores)
    # save_dict_to_json_file(scores, "data/json/marvel/final.json")
