from enum import Enum

class Actions(Enum):
    move = 0
    eat = 1
    attack = 2

class Agent (object):
    def take_turn(self):
        # common things that all agents would do
        pass

class Creature (Agent):
    def __init__(self):
        self.variables = 'blah'

    def take_turn(self):
        # common things that all creatures would do
        self.super()

    def sense_creatures(self):
        pass

    def sense_predators(self):
        creatures = self.sense_creatures()
        predators = [x for x in creatures if x.diet == "Creature"]
        return predators

    def do_action(self, response):
        response_type, parameters = response
        if response_type == Actions.move:
            direction, distance = parameters
            # ....

class Rabbit (Creature):
    def __init__(self, parents):
        # re: parents - would we want creature's attributes to be affected by its lineage?  we could if we want.
        self.diet = "Vegitation"
        self.sense_distance = 2

    def take_turn(self):
        self.super()
        response = None

        predators = self.sense_predators()





class Vegitation(Agent):
    def __init__(self):
        self.food_value = 0

    def take_turn(self):
        self.grow()

    def grow(self):
        self.food_value += 1