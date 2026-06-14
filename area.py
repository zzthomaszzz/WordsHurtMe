from enemy import *
from config import *

class AreaBase:
    def __init__(self, enemies, weights, time_per_prompt):
        self.enemies = enemies
        self.weights = weights
        self.time_per_prompt = time_per_prompt
        self.enemy_amount = random.randint(1, 5)

        self.enemies_list = None
        self.current_enemy = None
        self.set_enemy_combat_list()

    def set_enemy_combat_list(self):
        chosen_classes = random.choices(self.enemies, weights=self.weights, k=self.enemy_amount)
        self.enemies_list = [EnemyClass() for EnemyClass in chosen_classes]
        self.current_enemy = self.enemies_list[0]


class AreaHouse(AreaBase):
    def __init__(self):
        super().__init__([EnemyVillager, EnemyPariah, EnemyApostle, EnemyFanatic], [70, 10, 10, 10], TIME_PER_PROMPT_HOUSE)

class AreaMurkeyWater(AreaBase):
    def __init__(self):
        super().__init__([EnemyMurklurker, EnemyDominantMurklurker], [90, 10], TIME_PER_PROMPT_MURKEY_WATER)

class AreaBoatHouse(AreaBase):
    def __init__(self):
        super().__init__([EnemyPariah, EnemyVillager], [50, 50], TIME_PER_PROMPT_BOAT_HOUSE)

class AreaChapel(AreaBase):
    def __init__(self):
        super().__init__([EnemyFanatic, EnemyApostle, EnemyVillager, EnemyTeacher], [40, 30, 20, 10], TIME_PER_PROMPT_CHAPEL)

class AreaLighthouse(AreaBase):
    def __init__(self):
        super().__init__([EnemyLighthouse], [100], TIME_PER_PROMPT_LIGHTHOUSE)