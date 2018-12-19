import logging
from enum import Enum
from random import randint

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

    def cast(self, character, target, statistics, time):
        raise Exception("Not implemented")



class Spell(Action):
    def __init__(self, name, rank, cast_time, cooldown, resource_cost, dmg_type, effects):
        if not effects:
            raise Exception("spell got empty action list")

        Action.__init__(self, "%s (%s)"% (name, rank), Types.SPELL)
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.resource_cost = resource_cost
        self.dmg_type = dmg_type
        self.effects = []

        for effect_data in effects:
            self.effects.append(self.parse_effect(effect_data))


    def cast(self, character, target, statistics, time):
        total_damage = 0
        for effect in self.effects:
            total_damage += effect.cast(character, target, statistics, time)

        if total_damage == 0:
            logging.info("%.2f - [%s] %s" % (time.get_time()/1000,
                                             character,
                                             self))
        else:
            logging.info("%.2f - [%s] %s: %s" % (time.get_time()/1000,
                                                 character,
                                                 self,
                                                 total_damage))

    def parse_effect(self, effect_data):
        effect_type = effect_data[0]
        if effect_type is 0:
            return InstantDamage(effect_data[1],
                                 effect_data[2])
        elif effect_type is 1:
            return Dot(self.name,
                       effect_data[1],
                       effect_data[2],
                       effect_data[3],
                       effect_data[4])

        raise Exception("unkown effect type %s" % effect_type)



class AutoAttack(Action):
    def __init__(self, min_dmg, max_dmg):
        Action.__init__(self, "Auto Attack", Types.ATTACK)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def cast(self, character, target, statistics, time):
        damage = randint(self.min_dmg, self.max_dmg)
        logging.info("%.2f - [%s] %s: %s" % (time.get_time()/1000,
                                             character,
                                             self,
                                             damage))
        statistics.update_damage_done(damage)


class AutoShot(Action):
    # TODO damage should be calculated from character info...

    def __init__(self, min_dmg, max_dmg):
        Action.__init__(self, "Auto Shot", Types.SHOT)
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def cast(self, character, target, statistics, time):
        damage = randint(self.min_dmg, self.max_dmg)
        logging.info("%.2f - [%s] %s: %s" % (time.get_time()/1000,
                                             character,
                                             self,
                                             damage))
        statistics.update_damage_done(damage)





class InstantDamage:
    def __init__(self, min_dmg, max_dmg):
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def cast(self, character, target, statistics, time):
        damage = randint(self.min_dmg, self.max_dmg)
        statistics.update_damage_done(damage)
        return damage


class Dot:
    def __init__(self, name, min_dmg, max_dmg, interval, duration):
        self.name = name
        self.tick_dmg = min_dmg # TODO implement min and max dmg!
        self.duration = duration
        self.interval = interval

    def cast(self, character, target, statistics, time):
        target.add_dot(character, DotDebuff(self.name,
                                            self.tick_dmg,
                                            self.duration,
                                            self.interval,
                                            time))
        return 0


class DotDebuff:
    def __init__(self, name, tick_dmg, duration, interval, time):
        self.name = name
        self.tick_dmg = tick_dmg
        self.interval = interval
        self.end_time = time.get_time() + duration
        self.next_tick_time = time.get_time() + interval

    def get_damage(self, time):
        if time.get_time() >= self.next_tick_time:
            self.next_tick_time += self.interval
            return self.tick_dmg

        return None

    def timedout(self, time):
        return time.get_time() >= self.end_time
