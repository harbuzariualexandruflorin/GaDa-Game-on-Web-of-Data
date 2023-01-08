from rdflib import Namespace

from tools.scraper_macros import CARD_TYPES

API_NAMESPACE = 'https://gada.cards.game.namespace.com/'
EX = Namespace(API_NAMESPACE)
PREFIX_EX = "gada"
POKE = Namespace('https://triplydb.com/academy/pokemon/vocab/')
DBO = Namespace("http://dbpedia.org/ontology/")
DBR = Namespace("http://dbpedia.org/resource/")
DBC = Namespace("http://dbpedia.org/resource/Category:")
SWAPI = Namespace('https://swapi.co/vocabulary/')

STAR_TREK_PROP_DBPEDIA = {
    "warpCapableSpecies": "Warp",
    "humanoidSpecies": "Humanoid",
    "reptilianSpecies": "Reptilian",
    "avianSpecies": "Avian",
    "shapeshiftingSpecies": "Shapeshifting",
    "spaceborneSpecies": "Outer_space",
    "telepathicSpecies": "Telepathy",
    "alternateReality": "Alternate_reality"
}

POKEMON_TYPE_DBPEDIA = {
    'grass': 'Vegetation',
    'poison': 'Poison',
    'fire': 'Fire',
    'flying': 'Flight',
    'water': 'Water',
    'bug': 'Insect',
    'electric': 'Electricity',
    'ground': 'Dirt',
    'fairy': 'Fairy',
    'fighting': 'Combat',
    'psychic': 'Psychic',
    'rock': 'Rock_(geology)',
    'steel': 'Steel',
    'ice': 'Ice',
    'ghost': 'Ghost',
    'dragon': 'Dragon',
    'dark': 'Evil'
}

STAR_WARS_FILM_DBPEDIA = {
    'A New Hope': 'Star_Wars_Episode_IV:_A_New_Hope',
    'The Empire Strikes Back': 'The_Empire_Strikes_Back',
    'Return of the Jedi': 'Return_of_the_Jedi',
    'Revenge of the Sith': 'Star_Wars:_Episode_III_–_Revenge_of_the_Sith',
    'The Phantom Menace': 'Star_Wars:_Episode_I_–_The_Phantom_Menace',
    'Attack of the Clones': 'Star_Wars:_Episode_II_–_Attack_of_the_Clones'

}

MARVEL_RACES_DBPEDIA = {
    'Human': "Human",
    'Mutant': "Mutant_(Marvel_Comics)",
    'God': "God",
    'Eternal': "Eternals_(comics)",
    'Inhuman': "Inhumans",
    'Demon': "Demon",
    'Vampire': "Vampire_(Marvel_Comics)",
    'Symbiote': "Symbiote_(comics)",
    'Cyborg': "Cyborg",
    'Cosmic Entity': "Cosmic_entity_(Marvel_Comics)",
    'Flora Colossus': "Flora_colossus",
    'Demi-God': "Demigod",
    'Asgardian': "Asgard_(comics)",
    'Atlantean': "Homo_mermanus",
    'Animal': "Animal",
    'Alien': "Extraterrestrial_life",
    'Android': "Android_(robot)"
}
MARVEL_ALIGN_DBPEDIA = {
    "good": "Hero",
    "neutral": "Antihero",
    "bad": "Villain"
}

CARD_TYPES_CHART = {
    CARD_TYPES.teleport: [CARD_TYPES.flying, CARD_TYPES.dragon, CARD_TYPES.psychic, CARD_TYPES.fighting],
    CARD_TYPES.fighting: [CARD_TYPES.normal, CARD_TYPES.rock, CARD_TYPES.steel, CARD_TYPES.ice, CARD_TYPES.dark],
    CARD_TYPES.flying: [CARD_TYPES.fighting, CARD_TYPES.bug, CARD_TYPES.grass],
    CARD_TYPES.poison: [CARD_TYPES.grass, CARD_TYPES.fairy, CARD_TYPES.teleport],
    CARD_TYPES.ground: [CARD_TYPES.poison, CARD_TYPES.rock, CARD_TYPES.steel, CARD_TYPES.fire, CARD_TYPES.electric],
    CARD_TYPES.rock: [CARD_TYPES.flying, CARD_TYPES.bug, CARD_TYPES.fire, CARD_TYPES.ice],
    CARD_TYPES.bug: [CARD_TYPES.grass, CARD_TYPES.psychic, CARD_TYPES.dark],
    CARD_TYPES.ghost: [CARD_TYPES.psychic, CARD_TYPES.teleport],
    CARD_TYPES.steel: [CARD_TYPES.rock, CARD_TYPES.ice, CARD_TYPES.fairy],
    CARD_TYPES.fire: [CARD_TYPES.bug, CARD_TYPES.steel, CARD_TYPES.grass, CARD_TYPES.ice],
    CARD_TYPES.water: [CARD_TYPES.ground, CARD_TYPES.rock, CARD_TYPES.fire],
    CARD_TYPES.grass: [CARD_TYPES.ground, CARD_TYPES.rock, CARD_TYPES.water],
    CARD_TYPES.electric: [CARD_TYPES.flying, CARD_TYPES.water, CARD_TYPES.teleport],
    CARD_TYPES.psychic: [CARD_TYPES.fighting, CARD_TYPES.poison],
    CARD_TYPES.ice: [CARD_TYPES.flying, CARD_TYPES.ground, CARD_TYPES.grass, CARD_TYPES.dragon],
    CARD_TYPES.dragon: [CARD_TYPES.flying],
    CARD_TYPES.dark: [CARD_TYPES.ghost, CARD_TYPES.psychic],
    CARD_TYPES.fairy: [CARD_TYPES.fighting, CARD_TYPES.dragon, CARD_TYPES.dark, CARD_TYPES.teleport]
}
