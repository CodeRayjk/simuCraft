
class Status:
    IDLE, CASTING = range(2)



class CharacterHandler:
    def __init__(self, character):
        self.character = character
        self.current_status = Status.IDLE

    def update(self, time):
        pass

