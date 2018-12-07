from itertools import cycle
from model.actions import Spell, AutoShot

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
        if type(action) != Spell:
            return

        if action.cooldown > 0:
            self.cooldowns[action] = time.get_time() + action.cooldown

    def is_on_cooldown(self, action):
        return type(action) == Spell and action in self.cooldowns



class ActionPriority(ActionHandler):
    def __init__(self, actions):
        super(ActionPriority, self).__init__()
        self.actions = actions

    def get_next_action(self, time):
        self.update_cooldowns(time)

        for action in self.actions:
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


def get_action_handler(character):
    if character.name == "Rayjk":
        return ActionSequence([AutoShot(61, 114),
                               Spell("Arcane Shot (Rank 8)", 0.0, 6.0, 183, 183),
                               AutoShot(61, 114),
                               AutoShot(61, 114)])
    else:
        return ActionPriority([Spell("Shadowburn (Rank 6)", 0.0, 15.0, 450, 503),
                               Spell("Shadow Bolt (Rank 10)", 2.5, 0.0, 482, 539)])

    # [Spell("Searing Pain (Rank 6)", 1.5, 0.0, 204, 241)]

