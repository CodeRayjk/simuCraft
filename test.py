import unittest

from model.character import Character
from model.actions import Spell, AutoShot
from Engine.character_handler import ActionStatus
from Engine.simulation import SimulatedTime

class TestActionStatus(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestActionStatus, self).__init__(*args, **kwargs)
        self.character = Character("Gurkis")

    def test_casting(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        spell = Spell("Test Spell", 1, 0, 0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(spell, time)

        self.assertTrue(status.is_casting())


    def test_instant_cast(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        spell = Spell("Test Spell", 0, 0, 0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(spell, time)

        self.assertFalse(status.is_casting())

        status.action_done(time)
        status.set_new_action(spell, time)

        self.assertTrue(status.is_casting())


    def test_auto_shot(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        shot = AutoShot(0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(shot, time)

        self.assertFalse(status.is_casting())

        status.action_done(time)
        status.set_new_action(shot, time)

        self.assertTrue(status.is_casting())


    def test_update(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        spell = Spell("Test Spell", 1, 0, 0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(spell, time)

        self.assertTrue(status.is_casting())

        time.tick()
        status.update(time)

        self.assertFalse(status.is_casting())

        status.action_done(time)


    def test_instant_cast_and_auto_shot(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        spell = Spell("Test Spell", 0, 0, 0, 0)
        shot = AutoShot(0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(shot, time)
        status.action_done(time)

        self.assertFalse(status.is_casting())

        status.set_new_action(spell, time)

        self.assertTrue(status.is_casting())

        time.tick()
        status.update(time)

        self.assertFalse(status.is_casting())

        status.action_done(time)

        status.set_new_action(shot, time)

        self.assertTrue(status.is_casting())


    def test_long_spell(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        long_spell = Spell("Test Spell", 2000, 0, 0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(long_spell, time)

        self.assertTrue(status.is_casting())

        while time.get_time() < 2000:
            self.assertTrue(status.is_casting())
            time.tick()
            status.update(time)

        self.assertFalse(status.is_casting())

        status.action_done(time)


    def test_global_cooldown(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        instant_spell = Spell("Test Spell", 0, 0, 0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(instant_spell, time)

        self.assertFalse(status.is_casting())

        status.action_done(time)
        status.set_new_action(instant_spell, time)

        self.assertTrue(status.is_casting())

        while time.get_time() < status.globalcd:
            self.assertTrue(status.is_casting())
            time.tick()
            status.update(time)

        # one extra for latency
        time.tick()
        status.update(time)

        self.assertFalse(status.is_casting())

        status.action_done(time)


    def test_instant_and_cast(self):
        time = SimulatedTime(20000)
        status = ActionStatus(self.character)
        instant_spell = Spell("Test Spell", 0, 0, 0, 0)
        cast_spell = Spell("Test Spell", 500, 0, 0, 0)

        self.assertFalse(status.is_casting())

        status.set_new_action(instant_spell, time)

        self.assertFalse(status.is_casting())

        status.action_done(time)
        status.set_new_action(cast_spell, time)

        self.assertTrue(status.is_casting())

        while time.get_time() < status.globalcd + 500:
            self.assertTrue(status.is_casting())
            time.tick()
            status.update(time)

        # one extra for latency
        time.tick()
        status.update(time)

        self.assertFalse(status.is_casting())

        status.action_done(time)


if __name__ == '__main__':
    unittest.main()
