from http import HTTPStatus

import requests

from tools import *

FILMS_DICT = {}


def star_wars_get_film_dict(film_json):
    producers = film_json.get("producer", None)
    if producers is not None:
        producers = split_by_char(producers, ",")

    fid = film_json.get("episode_id", None)
    if fid is not None:
        fid = "star_wars:films:" + str(fid)
    return dict_keys_filter({
        "title": film_json.get("title", None),
        "id": fid,
        "director": film_json.get("director", None),
        "producers": producers,
        "release_date": film_json.get("release_date", None)
    })


def star_wars_get_films_api(films):
    films_info = []
    for film_url in films:
        if FILMS_DICT.get(film_url, None) is not None:
            films_info.append(FILMS_DICT[film_url])
            continue

        try:
            response = requests.get(film_url)
            if response.status_code != HTTPStatus.OK:
                print("ERROR STATUS CODE NOT OK IN api call " + film_url)
                continue
            film_json = json.loads(response.content.decode())
        except:
            print("ERROR IN api call " + film_url)
            continue

        film_dict = star_wars_get_film_dict(film_json)
        if len(film_dict.KEYS()) > 0:
            FILMS_DICT[film_url] = film_dict
            films_info.append(film_dict)

    return films_info if len(films_info) > 0 else None


def star_wars_get_planet_api(url):
    try:
        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            print("ERROR STATUS CODE NOT OK IN api call " + url)
            return None
        planet_json = json.loads(response.content.decode())
    except:
        print("ERROR IN api call " + url)
        return None

    if planet_json.get("name", None) is None:
        return None
    if planet_json["name"] == "unknown":
        return None

    result = dict_keys_filter({
        "name": planet_json["name"],
        "id": "star_wars:planets:" + get_endpoint_id(url),
        "climate": split_by_char(check_string_na(planet_json.get("climate", None), ["n/a", "unknown", "none"]), ","),
        "terrain": split_by_char(planet_json.get("terrain", None), ","),
        "surface_water": check_string_na(planet_json.get("surface_water", None), ["n/a", "unknown", "none"]),
    })
    if "unknown" in result.get("terrain", []):
        result["terrain"] = None
        result = dict_keys_filter(result)
    return result if len(result.KEYS()) > 0 else None


def star_wars_get_drivable_dict(drivable_json, drivable_class):
    return dict_keys_filter({
        "name": drivable_json.get("name", None),
        "length": drivable_json.get("length", None),
        "max_atmosphering_speed": check_string_na(drivable_json.get("max_atmosphering_speed", None), ["n/a", "unknown", "none"]),
        "crew": drivable_json.get("crew", None),
        "passengers": check_string_na(drivable_json.get("passengers", None), ["n/a", "unknown", "none"]),
        "hyperdrive_rating": drivable_json.get("hyperdrive_rating", None),
        "id": "star_wars:" + drivable_class + ":" + get_endpoint_id(drivable_json["url"])
    })


def star_wars_get_drivables_api(drivables, drivable_class):
    drivable_info = []
    for drivable_url in drivables:
        try:
            response = requests.get(drivable_url)
            if response.status_code != HTTPStatus.OK:
                print("ERROR STATUS CODE NOT OK IN api call " + drivable_url)
                continue
            drivable_json = json.loads(response.content.decode())
        except:
            print("ERROR IN api call " + drivable_url)
            continue

        drivable_dict = star_wars_get_drivable_dict(drivable_json, drivable_class)
        if len(drivable_dict.KEYS()) > 0:
            drivable_info.append(drivable_dict)

    return drivable_info if len(drivable_info) > 0 else None


def star_wars_get_species_dict(species_json):
    return dict_keys_filter({
        "name": species_json.get("name", None),
        "classification": check_string_na(species_json.get("classification", None), ["n/a", "unknown", "none"]),
        "average_lifespan": check_string_na(species_json.get("average_lifespan", None), ["n/a", "unknown", "none"]),
        "id": "star_wars:species:" + get_endpoint_id(species_json["url"])
    })


def star_wars_get_species_api(species):
    species_info = []
    for species_url in species:
        try:
            response = requests.get(species_url)
            if response.status_code != HTTPStatus.OK:
                print("ERROR STATUS CODE NOT OK IN api call " + species_url)
                continue
            species_json = json.loads(response.content.decode())
        except:
            print("ERROR IN api call " + species_url)
            continue

        species_dict = star_wars_get_species_dict(species_json)
        if len(species_dict.KEYS()) > 0:
            species_info.append(species_dict)
    return species_info if len(species_info) > 0 else None


def star_wars_get_person_api(person_json):
    person_dict = dict_keys_filter({
        "name": person_json["name"],
        "birth_year": check_string_na(person_json.get("birth_year", None), ["n/a", "unknown", "none"]),
        "eye_color": split_by_char(check_string_na(person_json.get("eye_color", None), ["n/a", "unknown", "none"]), ","),
        "nr_films": len(person_json.get("films", [])),
        "films": star_wars_get_films_api(person_json.get("films", [])),
        "gender": check_string_na(person_json.get("gender", None), ["n/a", "unknown", "none"]),
        "hair_color": split_by_char(check_string_na(person_json.get(
            "hair_color", None
        ), ["n/a", "unknown", "none"]), ","),
        "height": check_string_na(person_json.get("height", None), ["n/a", "unknown", "none"]),
        "mass": check_string_na(person_json.get("mass", None), ["n/a", "unknown", "none"]),
        "homeworld": star_wars_get_planet_api(person_json.get("homeworld", None)),
        "skin_color": split_by_char(check_string_na(person_json.get(
            "skin_color", None
        ), ["n/a", "unknown", "none"]), ","),
        "species": star_wars_get_species_api(person_json.get("species", [])),
        "starships": star_wars_get_drivables_api(person_json.get("starships", []), "starships"),
        "nr_starships": len(person_json.get("starships", [])),
        "vehicles": star_wars_get_drivables_api(person_json.get("vehicles", []), "vehicles"),
        "nr_vehicles": len(person_json.get("vehicles", [])),
        "id": "star_wars:" + get_endpoint_id(person_json["url"]),
    })

    entity = {}
    for s in person_dict.get("species", []):
        c = s.get("classification", None)
        if c is not None:
            entity[c] = True
    person_dict["types"] = get_entity_types(STAR_WARS_TYPES, entity)
    return dict_keys_filter(person_dict)


def star_wars_get_entities_api(url="https://swapi.dev/api/people/?page=%s"):
    all_people = {"people": []}
    current_ids = []

    page = 0
    while True:
        page += 1
        print("Star Wars people page " + str(page), " done! (82 people per page)")

        try:
            response = requests.get(url % str(page))
            if response.status_code != HTTPStatus.OK:
                return all_people
            people_json = json.loads(response.content.decode())

            for person in people_json["results"]:
                print(person)
                if person.get("name", None) is None or person.get("url", None) is None:
                    print("Skipping star wars person... No name/id found for person " + str(person))
                    continue
                if person["url"] in current_ids:
                    print("Skipping star wars person... Duplicate id found for person " + str(person))
                    continue

                person_dict = star_wars_get_person_api(person)
                if len(person_dict.KEYS()) > 0:
                    current_ids.append(person["url"])
                    all_people["people"].append(person_dict)
            if not people_json["next"]:
                break
        except Exception as ex:
            print("STAR WARS API SCRAPER EXCEPTION: ", ex)
    return all_people


def star_wars_get_score(all_people):
    return entities_get_score(STAR_WARS_VARS, all_people)


def star_wars_scrape_avatars():
    all_people = load_json_file_to_dict(file_path='data/json/star_wars/api_orig.json')
    avatar_people = entities_scrape_avatar(all_people, "star wars character", ["star", "wars"])
    save_dict_to_json_file(avatar_people, "data/json/star_wars/orig_avatar.json")


def star_wars_build_json():
    return
    # entities = star_wars_get_entities_api()
    # save_dict_to_json_file(entities, "data/json/star_wars/api_orig.json")
    # star_wars_scrape_avatars()
    # entities = load_json_file_to_dict("data/json/star_wars/orig_avatar.json")
    # scores = star_wars_get_score(entities)
    # check_range_score(scores)
    # save_dict_to_json_file(scores, "data/json/star_wars/final.json")
