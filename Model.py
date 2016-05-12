from Environment import *
import unittest

# basic stubs for how the model could be ran

class Model(object):
    def __init__(self, conf = {}):
        self.grid_size        = conf['grid_size']          if 'grid_size' in conf          else 100
        self.veg_den          = conf['vegitation_density'] if 'vegitation_density' in conf else .3
        self.creature_den     = conf['creature_density']   if 'creature_density' in conf   else .2
        self.carnivore_chance = conf['carnivore_chance']   if 'carnivore_chance' in conf   else .2
        self.omnivore_chance  = conf['omnivore_chance']    if 'omnivore_chance' in conf    else .2
        self.sim_length       = conf['sim_length']         if 'sim_length' in conf         else 1
        self.steps_day        = conf['steps_day']          if 'steps_day' in conf          else 1

        self.delta_t = 1 / float(self.steps_day)

    def run_simulation(self):
        self.env = Environment(self)

        for x in range (self.sim_length * self.steps_day):
            for agent in self.env.agents:
                # delta_t, x, and steps per day can be used if an agent should have different behaviors
                # at different times of day (if sim_length were days, and delta_t was 1/24,
                # then (x % steps_day) between 20 and 06 could be times that day-dwellers sleep, for example
                # Can be ignored if we'd rather not deal with it.
                agent.take_turn(self.delta_t, x, self.steps_day)

        # Report any interesting statistiscs, etc



class ModelTests(unittest.TestCase):
    def tests(self):
        m = Model({'grid_size': 100})
        m.run_simulation()

if __name__ == "__main__":
    tests = ModelTests()
    tests.tests()