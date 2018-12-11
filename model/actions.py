from enum import Enum

class Types(Enum):
    SPELL, SHOT, ATTACK = range(3)

class Action:
    def __init__(self, name, action_type):
        self.type = action_type
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name



class Spell(Action):
    def __init__(self, name, cast_time, cooldown, min_dmg, max_dmg):
        Action.__init__(self, name, Types.SPELL)
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg



class Dot(Action):
    def __init__(self, name, cast_time, cooldown, dot_dmg, duration):
        Action.__init__(self, name, Types.SPELL)
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.dot_dmg = dot_dmg
        self.duration = duration



class AutoAttack(Action):
    def __init__(self, min_dmg, max_dmg):
        Action.__init__(self, "Auto Attack", Types.ATTACK)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg



class AutoShot(Action):
    # TODO damage should be calculated from character info...

    def __init__(self, min_dmg, max_dmg):
        Action.__init__(self, "Auto Shot", Types.SHOT)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
