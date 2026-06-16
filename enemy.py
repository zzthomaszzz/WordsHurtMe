import random
from config import *

_NORMALIZE = str.maketrans({
    '‘': "'", '’': "'",
    '“': '"', '”': '"',
    '…': '...',
})

class EnemyBase:
    def __init__(self, name, health, prompt, loots, weights):
        self.name = name
        self.health = health
        self.max_health = health
        self.prompt = [p.translate(_NORMALIZE) for p in prompt]

        self.loots = loots
        self.weights = weights

        self.is_boss = False
        self.current_prompt = ""
        self.set_new_prompt()
        self.is_dead = False

    def set_new_prompt(self):
        choices = [p for p in self.prompt if p != self.current_prompt]
        self.current_prompt = random.choice(choices if choices else self.prompt)

    def get_loot(self):
        return random.choices(self.loots, weights=self.weights, k=1)[0]

class EnemyVillager(EnemyBase):
    def __init__(self):
        super().__init__("Villager", 30, [
            "I hear you, sacrifice. Stand still and embrace your fate",
            "The Light, the Light! Isn't it wonderful?",
            "You are here for a reason. Surrender to the Light!",
            "Your eyes led you to your destruction. darkness awaits",
            "The Lighthouse guides us! He provides us with sustenance!",
            "Run away, and one of us dies instead!",
        ], [
            None,
            ITEM_NAVIGATION_STICK,
            ITEM_MURKLURKER_CLUB,
            ITEM_SEAWEED_VEST,
            ITEM_WOODWEED_LEGGINGS,
            ITEM_LIGHTBALL,
        ], [10, 40, 10, 15, 15, 10])

class EnemyPariah(EnemyBase):
    def __init__(self):
        super().__init__("Pariah", 30, [
            "So the murklurkers didn't get you? I will",
            "At least you're not a murklurker",
            "We all have a purpose here. Even you... Even me",
            "I wish they could see the Light as I can. It's beautiful...",
            "The murklurkers fear me! You will soon know why."
        ], [
            ITEM_PARIAH_SPEAR,
            ITEM_STILT_BOX,
            ITEM_MURKLURKER_SKULL,
            ITEM_MURKLURKER_CAGE,
            ITEM_WOODWEED_LEGGINGS,
            ITEM_TORN_PIRATE_LEGGINGS,
            ITEM_BROKEN_PLANK,
        ], [8, 10, 17, 7, 26, 35, 15])

class EnemyApostle(EnemyBase):
    def __init__(self):
        super().__init__("Apostle", 30, [
            "O' Mighty Lighthouse, grant me strength!",
            "To reject the sins of the eyes! An act of salvation!",
            "Your death shall be quick! We offer you mercy!",
            "One moment of pain, and you rest in the Light for eternity!",
            "The Lighthouse is a kind God. You demonstrate His mercy."
        ], [
            None,
            ITEM_SACRIFICIAL_KNIFE,
            ITEM_CEREMONIAL_ROBE,
        ], [14, 36, 50])

class EnemyMurklurker(EnemyBase):
    def __init__(self):
        super().__init__("Murklurker", 30, [
            "Glarrrghrh",
            "Glurragh",
            "Garg Glurhgh",
            "Gurlaargghg",
            "Gurgar Glargh"
        ], [
            None,
            ITEM_MURKLURKER_TOOTH,
            ITEM_MURKLURKER_POOP,
            ITEM_MURKLURKER_FLESH,
            ITEM_SEAWEED,
            ITEM_MURKLURKER_CLUB,
            ITEM_MURKLURKER_SKULL,
        ], [20, 25, 2, 10, 8, 25, 10])

class EnemyDominantMurklurker(EnemyBase):
    def __init__(self):
        self.count = 0
        self.is_boss = True
        super().__init__("Dominant Murklurker", 60, [
            "Glaurrrgha Gulllgarrh",
            "Glarrrrghhhh Gugharrrrgh"
        ], [
            None,
            ITEM_MURKLURKER_TOOTH,
            ITEM_MURKLURKER_POOP,
            ITEM_MURKLURKER_FLESH,
            ITEM_SEAWEED,
            ITEM_MURKLURKER_CLUB,
            ITEM_MURKLURKER_SKULL,
        ], [20, 25, 2, 10, 8, 25, 10])

    def set_new_prompt(self):
        self.current_prompt = self.prompt[self.count]
        self.count += 1
        if self.count >= len(self.prompt):
            self.count = 0

class EnemyFanatic(EnemyBase):
    def __init__(self):
        super().__init__("Fanatic", 30, [
            "THE LIGGIGHIHT! IT'S BEAUTiFUL!",
            "FROMDARKNESS CoMeS LiiGht!",
            "THeLi.ght WiLL GuiuiDE YOu!",
            "ReMoVe YOURUR EyE!S GaIN SaLVATION!",
            "CoMEE!E! To T!H!E Liighht! Be FoRgiVEn!"
        ], [
            None,
            ITEM_LANTERN_FLAIL,
            ITEM_CLOAK_OF_DEVOTEE,
            ITEM_KNEELING_PADS,
            ITEM_LANTERN_HELMET,
            ITEM_WOODEN_LANTERN,
        ], [10, 20, 20, 17, 23, 10])

class EnemyTeacher(EnemyBase):
    def __init__(self):
        self.count = 0
        self.is_boss = True
        super().__init__("Teacher", 150, [
            "Leave. Do not corrupt the children! They have been saved by the Light!",
            "You have tarnished their sanctuary! We are not monsters!",
            "We are not insane! The Lighthouse grants us freedom from ourselves!",
            "You have to understand! Without us, who will take care of the children?",
            "They are so young, so lost. We are here for them! For all of them!"
        ], [
            None,
            ITEM_SEAWEED_HELMET,
        ], [60, 40])

    def set_new_prompt(self):
        self.current_prompt = self.prompt[self.count]
        self.count += 1
        if self.count >= len(self.prompt):
            self.count = 0

class EnemyLighthouse(EnemyBase):
    def __init__(self):
        self.count = 0
        self.is_boss = True
        super().__init__("Lighthouse", 120, [
            "Hello, Human. Have you come for the light? I cannot blame you for your desire.",
            "I have all the time in the world. Unlike you, death does not hinder me. Sit down and listen.",
            "The village you escaped. I am their nourishment. Their protection. Their guide. Their father. Their God.",
            "They came to me lost, scared, and confused. I freed them of their limitations, saved them from the Murklurkers."
        ], [
            ITEM_LIGHTHOUSE_HEART,
        ], [100])

    def set_new_prompt(self):
        self.current_prompt = self.prompt[self.count]
        self.count += 1
        if self.count >= len(self.prompt):
            self.count = 0
