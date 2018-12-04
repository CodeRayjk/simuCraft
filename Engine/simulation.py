from Engine.character_handler import CharacterHandler

class SimulatedTime:
    def __init__(self, total_time):
        self._current_time = 0
        self._time_per_tick = 0.001
        self._total_time = total_time

    def tick(self):
        self._current_time += self._time_per_tick

    def end_of_time(self):
        return self._current_time >= self._total_time


class Simulation:
    def __init__(self, total_time, target, characters):
        self.time = SimulatedTime(total_time)
        self.target = target
        self.character_handlers = []
        self.setup_charater_handlers(characters)

    def setup_charater_handlers(self, characters):
        for character in characters:
            self.character_handlers.append(CharacterHandler(character))


    def run(self):
        while not self.time.end_of_time():
            self.update_handlers()
            self.time.tick()


    def update_handlers(self):
        for handler in self.character_handlers:
            handler.update(self.time)
