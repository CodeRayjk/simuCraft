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


class DamageSpell(Action):
    def __init__(self, name, cast_time, cooldown, min_dmg, max_dmg):
        Action.__init__(self, name, Types.SPELL)
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg

    def cast(self, character, target, statistics, time):
        damage = randint(self.min_dmg, self.max_dmg)
        logging.info("%.2f - [%s] %s: %s" % (time.get_time()/1000,
                                             character,
                                             self,
                                             damage))
        statistics.update_damage_done(damage)


class DotEffect:
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


class Dot(Action):
    def __init__(self, name, cast_time, cooldown, tick_dmg, duration, interval):
        Action.__init__(self, name, Types.SPELL)
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.tick_dmg = tick_dmg
        self.duration = duration
        self.interval = interval

    def cast(self, character, target, statistics, time):
        logging.info("%.2f - [%s] %s" % (time.get_time()/1000,
                                         character,
                                         self))
        target.add_dot(character, DotEffect(self.name,
                                            self.tick_dmg,
                                            self.duration,
                                            self.interval,
                                            time))


class CombinedSpell(Action):
    def __init__(self, action_list):
        if len(action_list) == 0:
            raise Exception("CombinedSpell: empty action list")

        self.action_list = action_list
        Action.__init__(self, action_list[0].name, Types.SPELL)
        self.cast_time = action_list[0].cast_time
        self.cooldown = action_list[0].cooldown

    def cast(self, character, target, statistics, time):
        for actions in self.action_list:
            actions.cast(character, target, statistics, time)


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
