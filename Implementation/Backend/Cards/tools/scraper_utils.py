from data_scrapers.duckduckgo_image_scraper import search_image


def entities_scrape_avatar(entities, search_string, search_keywords):
    index = -1
    entities_key = list(entities.keys())[0]
    avatar_entities = {entities_key: []}

    for entity in entities[entities_key]:
        index += 1
        avatar = search_image(search_string + " " + entity["name"], search_keywords)
        if avatar is None:
            print("Skipping entity... No avatar found for  " + str(entity))
            continue
        entity["avatar"] = avatar
        print(index, entity)

        avatar_entities[entities_key].append(entity)
    return avatar_entities


def entities_get_score(variables, entities):
    entities_key = list(entities.keys())[0]
    for entity in entities[entities_key]:
        entity["score"] = get_entity_dict_score(variables, entity)
    return entities


def check_range_score(entities):
    entities_key = list(entities.keys())[0]
    max_score = entities[entities_key][0]["score"]
    min_score = entities[entities_key][0]["score"]
    max_count = 0
    min_count = 0

    for entity in entities[entities_key]:
        if entity["score"] > max_score:
            max_score = entity["score"]
        if entity["score"] < min_score:
            min_score = entity["score"]

    s = 0
    for entity in entities[entities_key]:
        s += entity["score"]
        if entity["score"] == max_score:
            max_count += 1
            print("MAX: ", entity)
        if entity["score"] == min_score:
            min_count += 1
            print("MIN: ", entity)
    print({
        "count": len(entities[entities_key]),
        "avg": s / len(entities[entities_key]),
        "max": {"value": max_score, "count": max_count},
        "min": {"value": min_score, "count": min_count}
    })


def get_entity_dict_score(variables, entity):
    if type(entity) is str:
        return int(variables.get(entity, 0))
    if type(entity) is not dict:
        return 0

    score = 0
    for k in entity.keys():
        if type(entity[k]) is str:
            try:
                score += int((variables.get(k, 0) / variables.get("DIV", 1)) * float(entity[k]))
                continue
            except:
                pass
            score += get_entity_dict_score(variables, entity[k])
            continue
        if type(entity[k]) is dict:
            score += get_entity_dict_score(variables, entity[k])
            continue
        if type(entity[k]) in [int, float]:
            score += int((variables.get(k, 0) / variables.get("DIV", 1)) * entity[k])
            continue
        if type(entity[k]) is bool:
            score += int((variables.get(k, 0) / variables.get("DIV", 1)) * int(entity[k]))
            continue
        if type(entity[k]) is list:
            for e in entity[k]:
                score += get_entity_dict_score(variables, e)
    return score + variables.get("ADJUST", 0)


def get_entity_types(variables, entity):
    types = []
    for k in entity.keys():
        if type(entity[k]) is bool and entity[k] is True:
            types += variables.get(k, [])
    types = list(dict.fromkeys([t.name for t in types]))
    return None if len(types) == 0 else types
