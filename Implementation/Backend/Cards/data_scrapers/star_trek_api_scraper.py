from http import HTTPStatus

import requests

from tools.common_utils import *
from tools.scraper_macros import *
from tools.scraper_utils import *


def star_trek_get_species_dict(species):
    species_dict = dict_keys_filter({
        "universe": "Star Trek",
        "name": species["name"],
        "id": "star_trek:" + species["uid"],
        "homeworld": adjust_none(species.get("homeworld", {}), {}).get("name", None),
        "quadrant": adjust_none(species.get("quadrant", {}), {}).get("name", None),
        "warpCapableSpecies": adjust_none(species.get("warpCapableSpecies", False), False),
        "extraGalacticSpecies": adjust_none(species.get("extraGalacticSpecies", False), False),
        "humanoidSpecies": adjust_none(species.get("humanoidSpecies", False), False),
        "reptilianSpecies": adjust_none(species.get("reptilianSpecies", False), False),
        "avianSpecies": adjust_none(species.get("avianSpecies", None), False),
        "nonCorporealSpecies": adjust_none(species.get("nonCorporealSpecies", False), False),
        "shapeshiftingSpecies": adjust_none(species.get("shapeshiftingSpecies", False), False),
        "spaceborneSpecies": adjust_none(species.get("spaceborneSpecies", False), False),
        "telepathicSpecies": adjust_none(species.get("telepathicSpecies", False), False),
        "transDimensionalSpecies": adjust_none(species.get("transDimensionalSpecies", False), False),
        "alternateReality": adjust_none(species.get("alternateReality", False), False)
    }, [None, False])
    species_dict["types"] = get_entity_types(STAR_TREK_TYPES, species)
    if species_dict["types"] in [["normal"], [], None]:
        return dict()
    return dict_keys_filter(species_dict, [None, False])


def star_trek_get_entities_api(url="http://stapi.co/api/v2/rest/species/search?pageSize=100&pageNumber=%s"):
    all_species = {"species": []}
    current_ids = []

    page = -1
    while True:
        page += 1
        print("Star Trek species page " + str(page), " done! (100 species per page)")

        try:
            response = requests.get(url % str(page))
            if response.status_code != HTTPStatus.OK:
                return all_species
            species_json = json.loads(response.content.decode())

            for species in species_json["species"]:
                if species.get("name", None) is None or species.get("uid", None) is None:
                    # print("Skipping star trek species... No name/id found for species " + str(species))
                    continue
                if species["uid"] in current_ids:
                    # print("Skipping star trek species... Duplicate id found for species " + str(species))
                    continue

                species_dict = star_trek_get_species_dict(species)
                if len(species_dict.keys()) > 0:
                    current_ids.append(species["uid"])
                    print(species_dict)
                    all_species["species"].append(species_dict)
            if species_json["page"]["lastPage"]:
                break
        except Exception as ex:
            print("STAR TREK API SCRAPER EXCEPTION: ", ex)
    return all_species


def star_trek_get_score(all_species):
    return entities_get_score(STAR_TREK_VARS, all_species)


def star_trek_scrape_avatars():
    all_species = load_json_file_to_dict(file_path='data/json/star_trek/api_orig.json')
    avatar_species = entities_scrape_avatar(all_species, "star trek species", ["star", "trek"])
    save_dict_to_json_file(avatar_species, "data/json/star_trek/orig_avatar.json")


def star_trek_build_json():
    return
    # entities = star_trek_get_entities_api()
    # save_dict_to_json_file(entities, "data/json/star_trek/api_orig.json")
    # star_trek_scrape_avatars()
    # entities = load_json_file_to_dict("data/json/star_trek/orig_avatar.json")
    # scores = star_trek_get_score(entities)
    # check_range_score(scores)
    # save_dict_to_json_file(scores, "data/json/star_trek/final.json")
