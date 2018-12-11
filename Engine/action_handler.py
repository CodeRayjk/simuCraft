import logging

from itertools import cycle
from model.actions import *

class ActionHandler:
    def __init__(self):
        self.cooldowns = {}

    def update_cooldowns(self, time):
        ready_spells = []
        for spell in self.cooldowns:
            if time.get_time() >= self.cooldowns[spell]:
                ready_spells.append(spell)

        for spell in ready_spells:
            del self.cooldowns[spell]

    def set_cooldown(self, action, time):
        if action.type != Types.SPELL:
            return

        if action.cooldown > 0:
            self.cooldowns[action] = time.get_time() + action.cooldown

    def is_on_cooldown(self, action):
        return action.type == Types.SPELL and action in self.cooldowns



class ActionPriority(ActionHandler):
    def __init__(self, actions, character, target):
        super(ActionPriority, self).__init__()
        self.actions = actions
        self.character = character
        self.target = target

    def get_next_action(self, time):
        self.update_cooldowns(time)

        for action in self.actions:
            if self.target.has_dot(self.character, action.name):
                continue

            if self.is_on_cooldown(action):
                continue

            self.set_cooldown(action, time)

            return action

        raise Exception("Bad action priority. All actions are on cooldown.")


class ActionSequence(ActionHandler):
    def __init__(self, sequence):
        super(ActionSequence, self).__init__()
        self.sequence = cycle(sequence)

    def get_next_action(self, time):
        self.update_cooldowns(time)
        action = next(self.sequence)

        if self.is_on_cooldown(action):
            raise Exception("Bad action sequence. Spell %s is on cooldown." % action)
        self.set_cooldown(action, time)

        return action


def get_action_handler(character, target):
    if character.name == "Rayjk":
        return ActionSequence([AutoShot(61, 114),
                               DamageSpell("Arcane Shot (Rank 8)", 0, 6000, 183, 183),
                               AutoShot(61, 114),
                               AutoAttack(31, 94)])
        # return ActionSequence([AutoShot(61, 114),
        #                        DamageSpell("Arcane Shot (Rank 8)", 0, 6000, 183, 183),
        #                        AutoShot(61, 114),
        #                        DamageSpell("Ap Shot (Rank 8)", 0, 6000, 183, 183),
        #                        AutoShot(61, 114)])
    else:
        immolate = CombinedSpell([DamageSpell("Immolate (Rank 8)", 2000, 0, 279, 279),
                                  Dot("Immolate (Rank 8)", 0, 0, 102, 15000, 3000)])
        corruption = Dot("Corruption (Rank 5)", 0, 0, 137, 18000, 3000)
        shadowburn = DamageSpell("Shadowburn (Rank 6)", 0, 15000, 450, 503)
        shadow_bolt = DamageSpell("Shadow Bolt (Rank 10)", 2500, 0, 482, 539)

        return ActionPriority([immolate,
                               corruption,
                               shadowburn,
                               shadow_bolt],
                              character,
                              target)
