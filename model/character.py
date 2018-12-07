class Character:
    def __init__(self, name, attack_speed=2.8):
        self.name = name
        self.attack_speed = attack_speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_attack_speed(self):
        return self.attack_speed
