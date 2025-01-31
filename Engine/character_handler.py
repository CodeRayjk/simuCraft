import logging

from model.actions import Types
from Engine.action_handler import get_action_handler

class CharacterHandler:
    def __init__(self, character, target):
        self.character = character
        self.target = target
        self.status = ActionStatus(self.character)
        self.action_handler = get_action_handler(character, target)
        self.current_action = None
        self.statistics = Statistics()

    def update(self, time):
        self.status.update(time)

        if self.current_action is not None and not self.status.is_casting():
            self.do_action(time)

        while self.current_action is None:
            self.handle_next_action(time)

        self.target.update_dots(time, self.statistics)

    def handle_next_action(self, time):
        self.current_action = self.action_handler.get_next_action(time)
        self.status.set_new_action(self.current_action, time)

        if not self.status.is_casting():
            self.do_action(time)

    def print_statistics(self):
        logging.info("[%s] %s" % (self.character,
                                  self.statistics))

    def do_action(self, time):
        self.status.action_done(time)
        self.current_action.cast(self.character, self.target, self.statistics, time)
        self.current_action = None


class ActionStatus:
    def __init__(self, character):
        self.ready_time = None
        self.cast_time = None
        self.auto_time = 0
        self.latency = 5
        self.globalcd = 1500
        self.character = character

    def update(self, time):
        if self.ready_time is None:
            return None

        if time.get_time() >= self.ready_time:
            self.ready_time = None

        if self.cast_time is not None and time.get_time() >= self.cast_time:
            self.cast_time = None

        return None

    def is_casting(self):
        return self.cast_time is not None

    def reset_auto_time(self, time):
        self.auto_time = time.get_time() + self.character.get_attack_speed()

    def set_new_action(self, action, time):
        if action.type == Types.SPELL:
            self.set_new_spell(action, time)
        else:
            self.set_new_auto(time)

    def set_new_spell(self, spell, time):
        base_time = self.ready_time or time.get_time()
        if spell.cast_time > 0:
            self.ready_time = base_time + max(spell.cast_time, self.globalcd) + self.latency
            self.cast_time = base_time + spell.cast_time

        else:
            self.cast_time = self.ready_time
            self.ready_time = base_time + self.globalcd + self.latency

    def set_new_auto(self, time):
        base_time = self.ready_time or time.get_time()
        if self.auto_time > time.get_time():
            self.ready_time = max(self.auto_time + self.latency, base_time)
            self.cast_time = self.auto_time
        else:
            self.ready_time = max(time.get_time() + self.latency, base_time)

    def action_done(self, time):
        # TODO research when auto timer is reset...
        self.reset_auto_time(time)



class Statistics:
    def __init__(self):
        self.total_damage_done = 0

    def update_damage_done(self, damage):
        self.total_damage_done += damage

    def __str__(self):
        return "Total damage done: %s" % self.total_damage_done
