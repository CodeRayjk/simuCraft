import logging

class ActionStatus:
    def __init__(self):
        self.current_action = None
        self.ready_time = None
        self.latency = 0.005

    def update(self, time):
        if self.current_action is None:
            return

        if time.get_time() >= self.ready_time:
            logging.info("%.2f - End casting: %s" % (time.get_time(), self.current_action.name))
            self.ready_time = None
            self.current_action = None

    def is_active(self):
        return self.current_action is not None

    def start_action(self, action, time):
        logging.info("%.2f - Start casting: %s" % (time.get_time(), action.name))

        if action.cast_time > 0:
            self.current_action = action
            self.ready_time = time.get_time() + action.cast_time + self.latency



class CharacterHandler:
    def __init__(self, character):
        self.character = character
        self.status = ActionStatus()
        self.action_handler = ActionHandler()

    def update(self, time):
        self.status.update(time)

        while not self.status.is_active():
            action = self.action_handler.get_next_action()
            self.status.start_action(action, time)



class ActionHandler:
    def get_next_action(self):
        return Action("Shadow Bolt (Rank 10)", 3)


class Action:
    def __init__(self, name, cast_time=0):
        self.name = name
        self.cast_time = cast_time
