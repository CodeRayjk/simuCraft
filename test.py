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



if __name__ == '__main__':
    unittest.main()
