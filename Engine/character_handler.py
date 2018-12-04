import logging

class ActionStatus:
    def __init__(self, character):
        self.current_action = None
        self.ready_time = None
        self.latency = 0.005
        self.character = character

    def update(self, time):
        if self.ready_time is None:
            return

        if time.get_time() >= self.ready_time:
            if self.current_action is not None:
                logging.info("%.2f - [%s] End casting: %s" % (time.get_time(),
                                                              self.character.name,
                                                              self.current_action.name))
            self.ready_time = None
            self.current_action = None

    def is_active(self):
        return self.ready_time is not None

    def start_action(self, action, time):
        if action.cast_time > 0:
            logging.info("%.2f - [%s] Start casting: %s" % (time.get_time(),
                                                            self.character.name,
                                                            action.name))
            self.current_action = action
            self.ready_time = time.get_time() + action.cast_time + self.latency

        else:
            logging.info("%.2f - [%s] Casting: %s" % (time.get_time(),
                                                      self.character.name,
                                                      action.name))
            self.ready_time = time.get_time() + 1 + self.latency


class CharacterHandler:
    def __init__(self, character):
        self.character = character
        self.status = ActionStatus(self.character)
        self.action_handler = ActionHandler(self.character)

    def update(self, time):
        self.status.update(time)

        while not self.status.is_active():
            action = self.action_handler.get_next_action()
            self.status.start_action(action, time)


class Character:
    def __init__(self, name):
        self.name = name


class ActionHandler:
    def __init__(self, character):
        self.character = character

        from itertools import cycle

        if self.character.name == "Rayjk":
            self.actions = cycle([Action("Searing Pain (Rank 6)", 1.5)])
        else:
            self.actions = cycle([Action("Shadow Bolt (Rank 10)", 2.5),
                                  Action("Shadowburn (Rank 6)", 0)])


    def get_next_action(self):
        return next(self.actions)


class Action:
    def __init__(self, name, cast_time=0):
        self.name = name
        self.cast_time = cast_time
