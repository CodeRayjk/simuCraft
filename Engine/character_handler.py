import logging
from random import randint

from model.spell import Spell


class CharacterHandler:
    def __init__(self, character, target):
        self.character = character
        self.target = target
        self.status = ActionStatus(self.character)
        self.action_handler = ActionHandler(self.character)
        self.damage_counter = DamageCounter(self.character, self.target)

    def update(self, time):
        spell = self.status.update(time)
        if spell is not None:
            self.damage_counter.update_damage_done(spell)

        while self.status.is_ready():
            self.cast_next_spell(time)

    def cast_next_spell(self, time):
        spell = self.action_handler.get_next_spell(time)
        self.status.set_ready_time(spell, time)

        if not self.status.is_casting():
            self.damage_counter.update_damage_done(spell)

    def print_statistics(self):
        logging.info("[%s] Damage done: %s" % (self.character,
                                               self.damage_counter.damage_done))


class ActionStatus:
    def __init__(self, character):
        self.current_spell = None
        self.ready_time = None
        self.cast_time = None
        self.latency = 0.005
        self.globalcd = 1
        self.character = character

    def update(self, time):
        if self.ready_time is None:
            return None

        if time.get_time() >= self.ready_time:
            self.ready_time = None

        if self.cast_time is not None and time.get_time() >= self.cast_time:
            logging.info("%.2f - [%s] Casting done: %s" % (time.get_time(),
                                                           self.character,
                                                           self.current_spell))
            self.cast_time = None
            spell = self.current_spell
            self.current_spell = None
            return spell

        return None

    def is_ready(self):
        return self.ready_time is None

    def is_casting(self):
        return self.cast_time is not None


    def set_ready_time(self, spell, time):
        logging.info("%.2f - [%s] Casting: %s" % (time.get_time(),
                                                  self.character,
                                                  spell))
        if spell.cast_time > 0:
            self.current_spell = spell
            self.ready_time = time.get_time() + max(spell.cast_time, self.globalcd) + self.latency
            self.cast_time = time.get_time() + spell.cast_time

        else:
            self.ready_time = time.get_time() + self.globalcd + self.latency



class ActionHandler:
    def __init__(self, character):
        self.character = character
        self.cooldowns = {}

        if self.character.name == "Rayjk":
            self.spells = [Spell("Searing Pain (Rank 6)", 1.5, 0.0, 204, 241)]
        else:
            self.spells = [Spell("Shadowburn (Rank 6)", 0.0, 15.0, 450, 503),
                           Spell("Shadow Bolt (Rank 10)", 2.5, 0.0, 482, 539)]
            # self.spells = [Spell("Shadowburn (Rank 6)", 0.0, 15.0, 450, 503)]
            # self.spells = [Spell("Shadow Bolt (Rank 10)", 2.5, 0, 482, 539)]

    def get_next_spell(self, time):
        self.update_cooldowns(time)

        for spell in self.spells:
            if self.is_on_cooldown(spell):
                continue

            self.set_cooldown(spell, time)
            return spell

        raise Exception("No spell available in priority.")

    def is_on_cooldown(self, spell):
        return spell in self.cooldowns

    def update_cooldowns(self, time):
        ready_spells = []
        for spell in self.cooldowns:
            if time.get_time() >= self.cooldowns[spell]:
                ready_spells.append(spell)

        for spell in ready_spells:
            del self.cooldowns[spell]

    def set_cooldown(self, spell, time):
        if spell.cooldown > 0:
            self.cooldowns[spell] = time.get_time() + spell.cooldown


class DamageCounter:
    def __init__(self, character, target):
        self.character = character
        self.target = target
        self.damage_done = 0

    def update_damage_done(self, spell):
        self.damage_done += randint(spell.min_dmg, spell.max_dmg)
