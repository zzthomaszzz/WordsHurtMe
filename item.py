class Item:
    def __init__(self, name, stat, value, equip_slot=None):
        self.name = name
        self.stat = stat
        self.value = value
        self.equip_slot = equip_slot  # "head", "body", "legs", "weapon", or None
