import pygame
from item import Item

if not pygame.get_init():
    pygame.display.init()


#Graphic
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60


#Main menu
BUTTON_START_WIDTH = 150
BUTTON_START_HEIGHT = 75
BUTTON_START_X = (WINDOW_WIDTH/2) - (BUTTON_START_WIDTH/2)
BUTTON_START_Y = (WINDOW_HEIGHT/2) - (BUTTON_START_HEIGHT/2)

#Main scene
BUTTON_HOUSE_WIDTH = 150
BUTTON_HOUSE_HEIGHT = 150
BUTTON_HOUSE_X = 1000
BUTTON_HOUSE_Y = 20

HOUSE_UNLOCKED = True
HOUSE_IMAGE_PATH = "assets/house.png"

BUTTON_MURKEY_WATER_WIDTH = 250
BUTTON_MURKEY_WATER_HEIGHT = 200
BUTTON_MURKEY_WATER_X = 200
BUTTON_MURKEY_WATER_Y = 400

MURKEY_WATER_UNLOCKED = True
MURKEY_WATER_IMAGE_PATH = "assets/murkey_water.png"

BUTTON_BOAT_HOUSE_WIDTH = 150
BUTTON_BOAT_HOUSE_HEIGHT = 125
BUTTON_BOAT_HOUSE_X = 750
BUTTON_BOAT_HOUSE_Y = 200

BOAT_HOUSE_UNLOCKED = False
BOAT_HOUSE_IMAGE_PATH = "assets/boat_house.png"

BUTTON_CHAPEL_WIDTH = 100
BUTTON_CHAPEL_HEIGHT = 120
BUTTON_CHAPEL_X = 300
BUTTON_CHAPEL_Y = 200

CHAPEL_UNLOCKED = False
CHAPEL_IMAGE_PATH = "assets/chapel.png"

BUTTON_LIGHTHOUSE_WIDTH = 100
BUTTON_LIGHTHOUSE_HEIGHT = 100
BUTTON_LIGHTHOUSE_X = 1100
BUTTON_LIGHTHOUSE_Y = 500

LIGHTHOUSE_UNLOCKED = False
LIGHTHOUSE_IMAGE_PATH = "assets/light_house.png"

BUTTON_OLD_CHAPEL_WIDTH = 130
BUTTON_OLD_CHAPEL_HEIGHT = 130
BUTTON_OLD_CHAPEL_X = 60
BUTTON_OLD_CHAPEL_Y = 20

OLD_CHAPEL_UNLOCKED = True
OLD_CHAPEL_IMAGE_PATH = "assets/chapel.png"

BACKGROUND_IMAGE_PATH = "assets/scene_main_background.png"

#Combat
BUTTON_INPUT_BOX_WIDTH = 700
BUTTON_INPUT_BOX_HEIGHT = 40
BUTTON_INPUT_BOX_X = (WINDOW_WIDTH/2) - (BUTTON_INPUT_BOX_WIDTH/2)
BUTTON_INPUT_BOX_Y = WINDOW_HEIGHT - BUTTON_INPUT_BOX_HEIGHT - 20

BUTTON_ENEMY_TEXT_BOX_WIDTH = 700
BUTTON_ENEMY_TEXT_BOX_HEIGHT = 40
BUTTON_ENEMY_TEXT_BOX_X = (WINDOW_WIDTH/2) - (BUTTON_ENEMY_TEXT_BOX_WIDTH/2)
BUTTON_ENEMY_TEXT_BOX_Y = 20

IMAGE_ENEMY_PATH = ""
IMAGE_ENEMY_X = 0
IMAGE_ENEMY_Y = 0

ENEMY_IMAGE_SIZE = 280
ENEMY_IMAGE_X = WINDOW_WIDTH // 2 - ENEMY_IMAGE_SIZE // 2
ENEMY_IMAGE_Y = 110

ENEMY_THUMBNAIL_SIZE = 64

ENEMY_IMAGE_PATHS = {
    "Murklurker":          "assets/murk_lurker.png",
    "Dominant Murklurker": "assets/dominant_murk_lurker.png",
    "Teacher":             "assets/teacher.png",
    "Pariah":              "assets/pariah.png",
    "Apostle":             "assets/apostle.png",
    "Villager":            "assets/villager.png",
    "Fanatic":             "assets/fanatic.png",
}

BUFFER_TIME = 3

#Prompt timers per area
TIME_PER_PROMPT_HOUSE = 12
TIME_PER_PROMPT_MURKEY_WATER = 8
TIME_PER_PROMPT_BOAT_HOUSE = 12
TIME_PER_PROMPT_CHAPEL = 12
TIME_PER_PROMPT_OLD_CHAPEL = 12
TIME_PER_PROMPT_LIGHTHOUSE = 20

#Wrong letter damage per area
DAMAGE_WRONG_LETTER_HOUSE = 30
DAMAGE_WRONG_LETTER_MURKEY_WATER = 30
DAMAGE_WRONG_LETTER_BOAT_HOUSE = 30
DAMAGE_WRONG_LETTER_CHAPEL = 30
DAMAGE_WRONG_LETTER_OLD_CHAPEL = 30
DAMAGE_WRONG_LETTER_LIGHTHOUSE = 15

#Damage flash
DAMAGE_FLASH_DURATION = 0.3
DAMAGE_PAUSE_DURATION = 2.0

#Player Stamina bar
PLAYER_STAMINA_BAR_X = WINDOW_WIDTH - 75
PLAYER_STAMINA_BAR_Y = 100
PLAYER_STAMINA_BAR_W = 25
PLAYER_STAMINA_BAR_H = 520

#Player HP bar
PLAYER_HP_BAR_X = 50
PLAYER_HP_BAR_Y = 100
PLAYER_HP_BAR_W = 25
PLAYER_HP_BAR_H = 520

#Skills
SKILL_CONTEMPLATION_COST = 20
SKILL_CONTEMPLATION_DURATION = 4.0

SKILL_DELIRIUM_COST = 25
SKILL_DELIRIUM_DURATION = 20.0

SKILL_CONCENTRATION_COST = 15
SKILL_CONCENTRATION_TIME_BONUS = 5.0

SKILL_DENIAL_COST = 30

SKILL_ACCEPTANCE_COST = 20
SKILL_ACCEPTANCE_DURATION = 15.0

#Timer bar
TIMER_BAR_X = BUTTON_INPUT_BOX_X
TIMER_BAR_Y = BUTTON_INPUT_BOX_Y - 20
TIMER_BAR_W = BUTTON_INPUT_BOX_WIDTH
TIMER_BAR_H = 12

#Skill slots
SKILL_SLOT_COUNT = 5
SKILL_SLOT_SIZE = 80
SKILL_SLOT_Y = TIMER_BAR_Y - 10 - SKILL_SLOT_SIZE

#Player base stats
PLAYER_BASE_HP = 100
PLAYER_BASE_STAMINA = 100
PLAYER_BASE_STAMINA_REGEN = 2.0

#Persistent inventory (mutated in-place across scenes)
player_inventory = []
player_equipment = {"head": None, "body": None, "legs": None, "weapon": None}

#Inventory button on main map
BUTTON_INVENTORY_WIDTH = 120
BUTTON_INVENTORY_HEIGHT = 40
BUTTON_INVENTORY_X = WINDOW_WIDTH - 130
BUTTON_INVENTORY_Y = WINDOW_HEIGHT - 50

#Items
#---Weapons---
ITEM_NAVIGATION_STICK = Item("Navigation Stick", "stamina", 10, "weapon",
    "Amazingly, these are not as common as you'd believe. Before they reach adulthood, the villagers slowly map out every section of the village through humiliating trial and error, trial and error which involves falling into the water more often than not. You assume this is for a child that hasn't gained that pattern recognition yet. Poor child.")
ITEM_MURKLURKER_CLUB = Item("Murklurker Club", "stamina", 15, "weapon",
    "A club with Murklurker teeth. Ironically, it's not very effective against the Murklurkers themselves. The Pariahs tried once. They never tried again.")
ITEM_PARIAH_SPEAR = Item("Pariah Spear", "stamina", 20, "weapon",
    "A crude spear crafted by the sighted pariahs for hunting. Its long reach makes it effective against Murklurkers, Pirates, and Island Tribesmen alike. To be killed by it is an ultimate insult.")
ITEM_SACRIFICIAL_KNIFE = Item("Sacrificial Knife", "stamina", 12, "weapon",
    "Wielded by the apostles to offer an unfortunate victim to the Lighthouse each week. Dying by it supposedly grants an eternity of bliss underneath the Lighthouse's gaze. It's probably best not to test the theory.")
ITEM_LANTERN_FLAIL = Item("Lantern Flail", "stamina", 25, "weapon",
    "Several small lanterns are tethered to a stick by especially strong seaweed. Contemplating how strange and impractical the weapon seems is a surefire way to be killed by it. It seems to amuse the Murklurkers.")

#---Body---
ITEM_SEAWEED_VEST = Item("Seaweed Vest", "health", 20, "body",
    "When the villagers have nothing better to do, they wander into the ocean and search for seaweed. Some of them have weaved clothing from it. It's cold and slimy, but surprisingly sturdy.")
ITEM_STILT_BOX = Item("Stilt Box", "health", 35, "body",
    "It's a blessing in disguise the villagers can't see, because this looks hideous. In theory, it's meant to help Pariahs when a Murklurker makes their way onto the stilts. Even the Murklurkers laugh at the outfit.")
ITEM_CEREMONIAL_ROBE = Item("Ceremonial Robe", "health", 36, "body",
    "An emerald-green robe damp with seawater and blood that the apostles wear during sacrifices. It offers little protection, but you'll look fabulous if you wear it.")
ITEM_CLOAK_OF_DEVOTEE = Item("Cloak of the Devotee", "health", 30, "body",
    "Contrary to the name, it's actually a poncho. A gaudily colored cloth poncho that somehow makes the cultists look even creepier. Only the most devoted are granted the privilege to wear it.")

#---Head---
ITEM_MURKLURKER_SKULL = Item("Murklurker Skull", "damage_reduction", 8, "head",
    "The pariahs sometimes wear these for bragging rights. The villagers never notice. They're blind.")
ITEM_MURKLURKER_CAGE = Item("Murklurker Cage", "damage_reduction", 15, "head",
    "A cage worn by pariahs to humiliate them. It is incredibly difficult to take off, but offers some protection against the Murklurkers.")
ITEM_LANTERN_HELMET = Item("Lantern Helmet", "damage_reduction", 13, "head",
    "Some of the villagers wear these to showcase their dedication to the Lighthouse. Some refuse to, fearing it would insult their God. Theological debates around this are common, and occasionally violent.")
ITEM_SEAWEED_HELMET = Item("Seaweed Helmet", "damage_reduction", 10, "head",
    "The blinded children are taught to make these to help them cope with their recent transformation. The quality is judged by the length of the seaweed and the amount of knots. They take it seriously.")

#---Legs---
ITEM_WOODWEED_LEGGINGS = Item("Woodweed Leggings", "stamina_regen", 10, "legs",
    "The villagers wear this for comfort and the pariahs wear it for protection. It doesn't really offer either, but in this village, nothing does.")
ITEM_TORN_PIRATE_LEGGINGS = Item("Torn Pirate Leggings", "stamina_regen", 8, "legs",
    "Stolen from the pirates in Trash Vortex during a raid. Those pirates didn't go down without a fight. They also didn't go down without ruining their own pants. Rude.")
ITEM_KNEELING_PADS = Item("Kneeling Pads", "stamina_regen", 12, "legs",
    "To be unable to pray to the Lighthouse is one of the most unforgivable sins in the village! Even the most psychotic of cultists understand the importance of proper leg-joint safety.")

#---Food / Misc---
ITEM_LIGHTBALL = Item("Lightball", "food", 21, description=
    "A ball of light, granted physical form by the Lighthouse for an unknown but likely nefarious reason. The good children get to play with these.")
ITEM_BROKEN_PLANK = Item("Broken Plank", "food", 14, description=
    "A plank that probably was meant to be part of a hut. One of the Pariahs dropped it, robbing it of its purpose. It's safe to say they were sacrificed for this mistake.")
ITEM_WOODEN_LANTERN = Item("Wooden Lantern", "food", 23, description=
    "Pariahs that are sacrificed are freed of their stigma, and granted the right to spend an eternity underneath the light. These lanterns are hung up to show their bravery.")
ITEM_MURKLURKER_TOOTH = Item("Murklurker Tooth", "food", 12, description=
    "These teeth slice through skin faster than most knives. Carrying these around without proper care is a good way to die of blood loss.")
ITEM_MURKLURKER_POOP = Item("Murklurker Poop", "food", 1, description=
    "Why the fuck would you pick this up? This is as horrific as you can imagine.")
ITEM_MURKLURKER_FLESH = Item("Murklurker Flesh", "food", 13, description=
    "The food of the Pariahs. It is heavy, looks awful, smells awful, tastes awful. It provides both food and water, but is only marginally better than dying from a lack of either.")
ITEM_SEAWEED = Item("Seaweed", "food", 2, description=
    "Gross, smelly seaweed. You could wear it on your nose to torment real estate agents if they still existed.")
ITEM_LIGHTHOUSE_HEART = Item("Lighthouse Heart", "food", 100, description=
    "The heart of an evil God. How the Lighthouse gained sentience or why it became so sadistic will be lost to time. This can be sold for a large amount of food... Or thrown into a fire.")