# Basic layout for how we could create an environment grid

from Terrain import *
from Creature import *
from Model import *
import random
import unittest

class Environment(object):
    def __init__(self, model):
        self.model = model
        self.grid = []
        self.grid_size = self.model.grid_size
        self.agents = []

        terrain_generator = None

        self.create_grid(terrain_generator)

    def create_grid(self, terrain_generator):
        if terrain_generator is None:
            # No intelligence to how terrain is created, just make random spaces
            # not sure how we'd want to implement intelligent terrain generation, some of the code
            # would need to change to give the terrain generator the information it needs (if we get to that point)
            terrain_generator = Gridpoint

        for y in range(self.grid_size):
            self.grid.append([])
            for x in range (self.grid_size):
                self.grid[y].append(terrain_generator())
                gp = self.grid[y][x]
                if random.random() < self.model.veg_den:
                    gp.agents.append(random_of("Vegitation")(y=y, x=x, model=self.model))
                if random.random() < self.model.creature_den:
                    if random.random() < self.model.carnivore_chance:
                        gp.agents.append(random_of("Carnivore")(y=y, x=x, model=self.model))
                    elif random.random() < self.model.omnivore_chance:
                        gp.agents.append(random_of("Omnivore")(y=y, x=x, model=self.model))
                    else:
                        gp.agents.append(random_of("Herbavore")(y=y, x=x, model=self.model))
                self.agents.extend(gp.agents)

class Gridpoint(object):
    def __init__(self, terrain_type = None):
        if terrain_type == None:
            # pick one at random
            #possible_options = Terrain.__subclasses__()
            #self.terrain = possible_options[random.randint(0, len(possible_options) - 1)]
            self.terrain = random_of('Terrain')
            self.agents = []


class EnvironmentTests(unittest.TestCase):
    def tests(self):
        print (Creature.__subclasses__())
        # m = Model()
        e = Environment(Model())
        self.assertEquals(e.grid_size, 100)
        print (e.grid_size)
        print (e.grid)
        print (e.agents)

def random_of(type):
    options = (eval(type + '.__subclasses__()'))
    return options[random.randint(0, len(options) - 1)]

if __name__ == "__main__":
    tests = EnvironmentTests()
    tests.tests()