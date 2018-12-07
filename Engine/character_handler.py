import logging
from random import randint

from model.actions import Spell
from Engine.action_handler import get_action_handler

class CharacterHandler:
    def __init__(self, character, target):
        self.character = character
        self.target = target
        self.status = ActionStatus(self.character)
        self.action_handler = get_action_handler(character)
        self.damage_counter = DamageCounter(self.character, self.target)

    def update(self, time):
        spell = self.status.update(time)
        if spell is not None:
            self.damage_counter.update_damage_done(spell, time)

        while self.status.is_ready():
            self.do_next_action(time)

    def do_next_action(self, time):
        action = self.action_handler.get_next_action(time)
        instant_action = self.status.set_new_action(action, time)

        if instant_action is not None:
            self.damage_counter.update_damage_done(instant_action, time)


    def print_statistics(self):
        logging.info("[%s] Damage done: %s" % (self.character,
                                               self.damage_counter.damage_done))


class ActionStatus:
    def __init__(self, character):
        self.current_action = None
        self.ready_time = None
        self.cast_time = None
        self.auto_time = 0.0
        self.latency = 0.005
        self.globalcd = 1.5
        self.character = character

    def update(self, time):
        if self.ready_time is None:
            return None

        if time.get_time() >= self.ready_time:
            self.ready_time = None
            if self.current_action is not None and type(self.current_action) != Spell:
                action = self.current_action
                self.current_action = None
                self.reset_auto_time(time)
                return action

        if self.cast_time is not None and time.get_time() >= self.cast_time:
            self.cast_time = None
            spell = self.current_action
            self.current_action = None
            return spell

        return None

    def is_ready(self):
        return self.ready_time is None

    def is_casting(self):
        return self.cast_time is not None

    def reset_auto_time(self, time):
        self.auto_time = time.get_time() + self.character.get_attack_speed()

    def set_new_action(self, action, time):
        if type(action) == Spell:
            return self.set_new_spell(action, time)
        else:
            return self.set_new_auto(action, time)

    def set_new_spell(self, spell, time):
        self.reset_auto_time(time) # TODO check when auto timer is reset. certain spells reset it...
        if spell.cast_time > 0:
            self.current_action = spell
            self.ready_time = time.get_time() + max(spell.cast_time, self.globalcd) + self.latency
            self.cast_time = time.get_time() + spell.cast_time
            return None

        else:
            self.ready_time = time.get_time() + self.globalcd + self.latency
            return spell

    def set_new_auto(self, action, time):
        ret_action = None
        if self.auto_time <= time.get_time():
            ret_action = action
            self.reset_auto_time(time)
            self.ready_time = time.get_time() + self.latency
        else:
            self.current_action = action
            self.ready_time = self.auto_time + self.latency

        return ret_action



class DamageCounter:
    def __init__(self, character, target):
        self.character = character
        self.calculator = DamageCalculator(character, target)
        self.damage_done = 0

    def update_damage_done(self, action, time):
        new_damage = self.calculator.calculate_damage(action)
        self.damage_done += new_damage

        logging.info("%.2f - [%s] %s: %s" % (time.get_time(),
                                             self.character,
                                             action,
                                             new_damage))


class DamageCalculator:
    def __init__(self, character, target):
        self.character = character
        self.target = target

    def calculate_damage(self, action):
        return randint(action.min_dmg, action.max_dmg)
