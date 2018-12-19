import logging

class Character:
    def __init__(self, name, attack_speed=2800):
        self.name = name
        self.attack_speed = attack_speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_attack_speed(self):
        return self.attack_speed


class Target:
    def __init__(self):
        self.dots = {}

    def add_dot(self, character, dot):
        self.dots.setdefault(character, []).append(dot)

    def has_dot(self, character, dot_name):
        for dot in self.dots.get(character, []):
            if dot.name == dot_name:
                return True

        return False


    def update_dots(self, time, statistics):
        for character in self.dots:
            timedout_dots = []
            for dot in self.dots[character]:
                damage = dot.get_damage(time)
                if damage is not None:
                    statistics.update_damage_done(damage)
                    logging.info("%.2f - [%s] %s: %s" % (time.get_time()/1000,
                                                         character,
                                                         dot.name,
                                                         damage))
                if dot.timedout(time):
                    timedout_dots.append(dot)

            for dot in timedout_dots:
                self.dots[character].remove(dot)
