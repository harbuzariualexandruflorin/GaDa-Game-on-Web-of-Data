from enum import Enum

from tools import load_json_file_to_dict

KEYS = load_json_file_to_dict("data/keys/api_keys.json")
MARVEL_API_KEYS = KEYS["MARVEL"]
SUPERHERO_API_KEY = KEYS["SUPERHERO"]

CARD_TYPES = Enum('PowerType', [
    'grass', 'poison', 'fire', 'flying', 'water', 'bug', 'normal',
    'electric', 'ground', 'fairy', 'fighting', 'psychic',
    'rock', 'steel', 'ice', 'ghost', 'dragon', 'dark', 'teleport'
])

POKEMON_VARS = {
    "nr_abilities": 1,
    "experience": 4,
    "nr_forms": 2,
    "height": 2,
    "nr_moves": 5,
    "attack": 8,
    "defense": 7,
    "hp": 6,
    "special_attack": 9,
    "special_defense": 8,
    "speed": 6,
    "weight": 1,
    "DIV": 17.6
}

STAR_TREK_VARS = {
    "warpCapableSpecies": 9,
    "extraGalacticSpecies": 8,
    "humanoidSpecies": 3,
    "reptilianSpecies": 4,
    "avianSpecies": 4,
    "nonCorporealSpecies": 7,
    "shapeshiftingSpecies": 6,
    "spaceborneSpecies": 6,
    "telepathicSpecies": 7,
    "transDimensionalSpecies": 8,
    "alternateReality": 7,
    "DIV": 0.03
}
STAR_TREK_TYPES = {
    "warpCapableSpecies": [CARD_TYPES.teleport],
    "extraGalacticSpecies": [CARD_TYPES.teleport],
    "humanoidSpecies": [CARD_TYPES.normal],
    "reptilianSpecies": [CARD_TYPES.fighting],
    "avianSpecies": [CARD_TYPES.flying],
    "nonCorporealSpecies": [CARD_TYPES.flying, CARD_TYPES.ghost],
    "shapeshiftingSpecies": [CARD_TYPES.fairy],
    "spaceborneSpecies": [CARD_TYPES.dark, CARD_TYPES.flying],
    "telepathicSpecies": [CARD_TYPES.psychic],
    "transDimensionalSpecies": [CARD_TYPES.teleport],
    "alternateReality": [CARD_TYPES.teleport]
}

STAR_WARS_VARS = {
    "male": 300,
    "female": 50,
    "hermaphrodite": 100,
    "height": 4,
    "mass": 2,
    "surface_water": 4,
    "arid": 200,
    "polluted": 100,
    "superheated": 200,
    "subartic": 100,
    "artic": 200,
    "frigid": 100,
    "nr_films": 6,
    "nr_starships": 8,
    "nr_vehicles": 7,
    "crew": 5,
    "passengers": 4,
    "length": 3,
    "max_atmosphering_speed": 6,
    "hyperdrive_rating": 6,
    "average_lifespan": 9,
    "indefinite": 90,
    "artificial": 100,
    "mammal": 50,
    "gastropod": 50,
    "amphibian": 150,
    "reptile": 100,
    "mammals": 50,
    "insectoid": 100,
    "reptilian": 100,
    "sentient": 600,
    "DIV": 500
}
STAR_WARS_TYPES = {
    "artificial": [CARD_TYPES.steel, CARD_TYPES.electric],
    "mammal": [CARD_TYPES.normal],
    "gastropod": [CARD_TYPES.ground],
    "reptile": [CARD_TYPES.fighting],
    "amphibian": [CARD_TYPES.water],
    "mammals": [CARD_TYPES.normal],
    "insectoid": [CARD_TYPES.flying, CARD_TYPES.bug],
    "reptilian": [CARD_TYPES.fighting]
}

MARVEL_VARS = {
    "nr_comics": 8,
    "nr_stories": 8,
    "nr_events": 8,
    "intelligence": 6,
    "strength": 8,
    "speed": 5,
    "durability": 6,
    "power": 9,
    "combat": 7,
    "nr_aliases": 5,
    "good": 100,
    "bad": 200,
    "neutral": 150,
    "Male": 100,
    "Female": 50,
    "height": 4,
    "weight": 3,
    "DIV": 10
}
MARVEL_TYPES = {
    'Mutant': [CARD_TYPES.fighting],
    'God': [CARD_TYPES.flying, CARD_TYPES.fairy, CARD_TYPES.fighting, CARD_TYPES.psychic, CARD_TYPES.teleport],
    'Eternal': [CARD_TYPES.fairy, CARD_TYPES.fighting, CARD_TYPES.psychic],
    'Inhuman': [CARD_TYPES.fighting],
    'Demon': [CARD_TYPES.fire, CARD_TYPES.dark, CARD_TYPES.fighting],
    'Vampire': [CARD_TYPES.dark, CARD_TYPES.fairy, CARD_TYPES.poison],
    'Symbiote': [CARD_TYPES.dark, CARD_TYPES.fighting, CARD_TYPES.poison],
    'Cyborg': [CARD_TYPES.electric, CARD_TYPES.steel],
    'Radiation': [CARD_TYPES.poison],
    'Cosmic Entity': [CARD_TYPES.flying, CARD_TYPES.dark, CARD_TYPES.teleport],
    'Demi-God': [CARD_TYPES.fighting],
    'Asgardian': [CARD_TYPES.fighting],
    'Animal': [CARD_TYPES.ground],
    'Alien': [CARD_TYPES.dark],
    'Android': [CARD_TYPES.electric, CARD_TYPES.steel]
}
