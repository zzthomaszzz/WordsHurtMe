import random
from item import Item

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
            "The Light, the Light! Isn’t it wonderful?",
            "You are here for a reason. Surrender to the Light!",
            "Your eyes led you to your destruction. darkness awaits",
            "The Lighthouse guides us! He provides us with sustenance!",
            "Run away, and one of us dies instead!",
        ], [
            None,
            Item("Murklurker Club",   "stamina",       15, "weapon", "A club with Murklurker teeth. Ironically, it’s not very effective against the Murklurkers themselves. The Pariahs tried once. They never tried again."),
            Item("Seaweed Vest",      "health",        20, "body",   "When the villagers have nothing better to do, they wander into the ocean and search for seaweed. Some of them have weaved clothing from it. It’s cold and slimy, but surprisingly sturdy."),
            Item("Woodweed Leggings", "stamina_regen", 10, "legs",   "The villagers wear this for comfort and the pariahs wear it for protection. It doesn’t really offer either, but in this village, nothing does."),
        ], [22, 19, 22, 37])

class EnemyPariah(EnemyBase):
    def __init__(self):
        super().__init__("Pariah", 30, [
            "So the murklurkers didn’t get you? I will",
            "At least you’re not a murklurker",
            "We all have a purpose here. Even you... Even me",
            "I wish they could see the Light as I can. It’s beautiful…",
            "The murklurkers fear me! You will soon know why."
        ], [
            Item("Pariah Spear",         "stamina",          20, "weapon", "A crude spear crafted by the sighted pariahs for hunting. Its long reach makes it effective against Murklurkers, Pirates, and Island Tribesmen alike. To be killed by it is an ultimate insult."),
            Item("Stilt Box",            "health",           35, "body",   "It’s a blessing in disguise the villagers can’t see, because this looks hideous. In theory, it’s meant to help Pariahs when a Murklurker makes their way onto the stilts. Even the Murklurkers laugh at the outfit."),
            Item("Murklurker Skull",     "damage_reduction",  8, "head",   "The pariahs sometimes wear these for bragging rights. The villagers never notice. They’re blind."),
            Item("Murklurker Cage",      "damage_reduction", 15, "head",   "A cage worn by pariahs to humiliate them. It is incredibly difficult to take off, but offers some protection against the Murklurkers."),
            Item("Woodweed Leggings",    "stamina_regen",    10, "legs",   "The villagers wear this for comfort and the pariahs wear it for protection. It doesn’t really offer either, but in this village, nothing does."),
            Item("Torn Pirate Leggings", "stamina_regen",     8, "legs",   "Stolen from the pirates in Trash Vortex during a raid. Those pirates didn’t go down without a fight. They also didn’t go down without ruining their own pants. Rude."),
        ], [8, 10, 17, 7, 26, 35])

class EnemyApostle(EnemyBase):
    def __init__(self):
        super().__init__("Apostle", 30, [
            "O’ Mighty Lighthouse, grant me strength!",
            "To reject the sins of the eyes! An act of salvation!",
            "Your death shall be quick! We offer you mercy!",
            "One moment of pain, and you rest in the Light for eternity!",
            "The Lighthouse is a kind God. You demonstrate His mercy."
        ], [
            None,
            Item("Sacrificial Knife", "stamina", 12, "weapon", "Wielded by the apostles to offer an unfortunate victim to the Lighthouse each week. Dying by it supposedly grants an eternity of bliss underneath the Lighthouse’s gaze. It’s probably best not to test the theory."),
        ], [64, 36])

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
            Item("Murklurker Tooth", "food",  12, description="These teeth slice through skin faster than most knives. Carrying these around without proper care is a good way to die of blood loss."),
            Item("Murklurker Poop",  "food",   1, description="Why the fuck would you pick this up? This is as horrific as you can imagine."),
        ], [66, 33, 1])

class EnemyDominantMurklurker(EnemyBase):
    def __init__(self):
        self.count = 0
        self.is_boss = True
        super().__init__("Dominant Murklurker", 60, [
            "Glaurrrgha Gulllgarrh Guuuuuragh",
            "Glarrrrghhhh Gugharrrrgh Guhargh"
        ], [
            None,
            Item("Murklurker Tooth", "food",  12, description="These teeth slice through skin faster than most knives. Carrying these around without proper care is a good way to die of blood loss."),
            Item("Murklurker Poop",  "food",   1, description="Why the fuck would you pick this up? This is as horrific as you can imagine."),
        ], [66, 33, 1])

    def set_new_prompt(self):
        self.current_prompt = self.prompt[self.count]
        self.count += 1
        if self.count >= len(self.prompt):
            self.count = 0

class EnemyFanatic(EnemyBase):
    def __init__(self):
        super().__init__("Fanatic", 30, [
            "THE LIGGIGHIHT! IT’S BEAUTiFUL!",
            "FROMDARKNESS CoMeS LiiGht!",
            "THeLi.ght WiLL GuiuiDE YOu!",
            "ReMoVe YOURUR EyE!S GaIN SaLVATION!",
            "CoMEE!E! To T!H!E Liighht! Be FoRgiVEn!"
        ], [
            None,
            Item("Lantern Flail",        "stamina",       25, "weapon", "Several small lanterns are tethered to a stick by especially strong seaweed. Contemplating how strange and impractical the weapon seems is a surefire way to be killed by it. It seems to amuse the Murklurkers."),
            Item("Cloak of the Devotee", "health",        30, "body",   "Contrary to the name, it’s actually a poncho. A gaudily colored cloth poncho that somehow makes the cultists look even creepier. Only the most devoted are granted the privilege to wear it."),
            Item("Kneeling Pads",        "stamina_regen", 12, "legs",   "To be unable to pray to the Lighthouse is one of the most unforgivable sins in the village. Even the most psychotic of cultists understand the importance of proper leg-joint safety."),
        ], [14, 28, 28, 30])

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
        ], [None], [100])


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
        ], [Item("Lighthouse Heart", "food", 100, description="The heart of an evil God. How the Lighthouse gained sentience or why it became so sadistic will be lost to time. This can be sold for a large amount of food... Or thrown into a fire.")], [100])

    def set_new_prompt(self):
        self.current_prompt = self.prompt[self.count]
        self.count += 1
        if self.count >= len(self.prompt):
            self.count = 0