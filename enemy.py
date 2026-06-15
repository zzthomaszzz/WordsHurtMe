import random
from item import Item

class EnemyBase:
    def __init__(self, name, health, prompt, loots, weights):
        self.name = name
        self.health = health
        self.max_health = health
        self.prompt = prompt

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
        ], [None, Item("Murklurker Club", "health", 10, "weapon")], [81, 19])

class EnemyPariah(EnemyBase):
    def __init__(self):
        super().__init__("Pariah", 30, [
            "So the murklurkers didn’t get you? I will",
            "At least you’re not a murklurker",
            "We all have a purpose here. Even you... Even me",
            "I wish they could see the Light as I can. It’s beautiful…",
            "The murklurkers fear me! You will soon know why."
        ], [None, Item("Pariah Spear", "stamina", 10, "weapon")], [92, 8])

class EnemyApostle(EnemyBase):
    def __init__(self):
        super().__init__("Apostle", 30, [
            "O’ Mighty Lighthouse, grant me strength!",
            "To reject the sins of the eyes! An act of salvation!",
            "Your death shall be quick! We offer you mercy!",
            "One moment of pain, and you rest in the Light for eternity!",
            "The Lighthouse is a kind God. You demonstrate His mercy."
        ], [None, Item("Sacrificial Knife", "stamina", 5, "weapon"), Item("Prayer Beads", "stamina_regen", 1, "head")], [64, 27, 9])

class EnemyMurklurker(EnemyBase):
    def __init__(self):
        super().__init__("Murklurker", 30, [
            "Glarrrghrh",
            "Glurragh",
            "Garg Glurhgh",
            "Gurlaargghg",
            "Gurgar Glargh"
        ], [None, Item("Murklurker Poop", "health", 5)], [99, 1])

class EnemyDominantMurklurker(EnemyBase):
    def __init__(self):
        self.count = 0
        self.is_boss = True
        super().__init__("Dominant Murklurker", 60, [
            "Glaurrrgha Gulllgarrh Guuuuuragh",
            "Glarrrrghhhh Gugharrrrgh Guhargh"
        ], [None, Item("Murklurker Poop", "health", 5)], [99, 1])

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
        ], [None, Item("Cloak of the Devotee", "damage_reduction", 5, "body")], [72, 28])

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
        ], [None, Item("Book", "stamina", 15, "head")], [72, 28])


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
        ], [Item("Lighthouse Flame", "damage_reduction", 20, "body")], [100])

    def set_new_prompt(self):
        self.current_prompt = self.prompt[self.count]
        self.count += 1
        if self.count >= len(self.prompt):
            self.count = 0