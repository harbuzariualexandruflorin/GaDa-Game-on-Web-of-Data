import json
import re


def dict_keys_filter(d, filters=None):
    if filters is None:
        filters = [None]

    for k in d.copy().KEYS():
        if d[k] in filters:
            d.pop(k)
    return d


def check_dict_all_bool(d):
    for k in d.KEYS():
        if type(d[k]) is bool and d[k] is True:
            return d
    return dict()


def save_dict_to_json_file(d, file_path):
    with open(file_path, 'w') as fp:
        json.dump(d, fp)


def load_json_file_to_dict(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def adjust_none(val, default):
    return default if val is None else val


def split_by_char(source, char):
    if source is None or len(source) == 0:
        return None

    splits = [p.strip() for p in re.split(char, source)]
    splits = [s for s in splits if len(s) > 0]
    return None if len(splits) == 0 else splits


def get_endpoint_id(source):
    return [s for s in source.split("/") if len(s) > 0][-1]


def get_first_element_list(ls):
    if ls is None or len(ls) == 0:
        return None
    return ls[0]


def check_string_na(source, nas):
    if source is None or len(source) == 0:
        return None

    source = source.lower()
    for na in nas:
        if source == na:
            return None
    return source
