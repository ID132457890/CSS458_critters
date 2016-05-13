from enum import Enum

class Agent (object):
    def __init__(self, y, x, model):
        self.location = (y,x)
        print ("%d,%d" % (y,x))

    def take_turn(self, delta_t, step, steps_day):
        # common things that all agents would do
        print(self)

class Creature (Agent):
    def __init__(self, y, x, model):
        Agent.__init__(self, y, x, model)
        self.variables = 'blah'

    def take_turn(self, delta_t, step, steps_day):
        # common things that all creatures would do
        super(Creature, self).take_turn(delta_t, step, steps_day)

    def sense_creatures(self):
        return []

    def sense_predators(self):
        creatures = self.sense_creatures()
        predators = [x for x in creatures if x.diet == "Creature"]
        return predators

    def do_action(self, response):
        pass

class Herbavore (Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

class Carnivore (Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

class Omnivore(Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

class Rabbit (Herbavore):
    def __init__(self, y, x, model, parents = None):
        # re: parents - would we want creature's attributes to be affected by its lineage?  we could if we want.
        Herbavore.__init__(self, y, x, model)
        self.sense_distance = 2

    def take_turn(self, delta_t, step, steps_day):
        super(Rabbit, self).take_turn(delta_t, step, steps_day)
        response = None
        predators = self.sense_predators()

class Wolf (Carnivore):
    pass

class Hog (Omnivore):
    pass

class Vegitation(Agent):
    def __init__(self, y, x, model):
        Agent.__init__(self, y, x, model)
        self.food_value = 0
        self.model = model

    def take_turn(self, delta_t, step, steps_day):
        super(Vegitation, self).take_turn(delta_t, step, steps_day)
        self.grow(delta_t)

    def grow(self, delta_t):
        self.food_value += 1 * delta_t

class EdiblePlant(Vegitation):
    def __init__(self, y, x, model):
        Vegitation.__init__(self, y, x, model)