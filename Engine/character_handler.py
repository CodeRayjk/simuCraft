import logging

class ActionStatus:
    def __init__(self, character):
        self.current_action = None
        self.ready_time = None
        self.cast_time = None
        self.latency = 0.005
        self.globalcd = 1
        self.character = character

    def update(self, time):
        if self.ready_time is None:
            return

        if self.cast_time is not None and time.get_time() >= self.cast_time:
            logging.info("%.2f - [%s] Casting done: %s" % (time.get_time(),
                                                           self.character.name,
                                                           self.current_action.name))
            self.current_action = None
            self.cast_time = None

        if time.get_time() >= self.ready_time:
            self.ready_time = None

    def is_active(self):
        return self.ready_time is not None

    def start_action(self, action, time):
        logging.info("%.2f - [%s] Casting: %s" % (time.get_time(),
                                                  self.character.name,
                                                  action.name))
        if action.cast_time > 0:
            self.current_action = action
            self.ready_time = time.get_time() + max(action.cast_time, self.globalcd) + self.latency
            self.cast_time = time.get_time() + action.cast_time

        else:
            self.ready_time = time.get_time() + self.globalcd + self.latency


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
