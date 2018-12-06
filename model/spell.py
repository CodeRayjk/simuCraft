class Spell:
    def __init__(self, name, cast_time, cooldown, min_dmg, max_dmg):
        self.name = name
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
