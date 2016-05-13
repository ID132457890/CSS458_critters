from Actions import *
import random

class Agent (object):
    def __init__(self, y, x, model):
        self.location = (y,x)
        self.model = model

    def take_turn(self, delta_t, step, steps_day):
        # No actions defined for the agent type if this is reached
        return NoAction()

    def daily_agent_maintenance(self):
        pass

class Creature (Agent):
    def __init__(self, y, x, model):
        Agent.__init__(self, y, x, model)
        self.movement_speed = 2
        self.air_movement = False
        self.surface_movement = True
        self.variables = 'blah'
        self.hydration = 40.0
        self.energy = 40.0
        self.daily_hydration_usage = 0.3
        self.daily_energy_usage = 0.3
        self.health = 1.0
        self.food_value = 1.0
        self.alive = True

    def take_turn(self, delta_t, step, steps_day):
        return super(Creature, self).take_turn(delta_t, step, steps_day)

    def daily_agent_maintenance(self):
        if self.alive == True:
            self.energy -= self.daily_energy_usage
            self.hydration -= self.daily_hydration_usage
            if min(self.energy, self.hydration) <= 0:
                print ("%r died" % self)
                self.alive = False
                self.movement_speed = 0
        else:
            self.food_value -= .5
            if self.food_value <= 0:
                self.model.env.remove_agent(self)
                print("%r rotted away" % self)

    def sense_creatures(self):
        return []

    def sense_predators(self):
        creatures = self.sense_creatures()
        predators = [x for x in creatures if x.diet == "Creature"]
        return predators

    def possible_movements(self):
        y = self.location[0]
        x = self.location[1]
        movement_choices = ((y-1,x-1), (y-1,x-1), (y+1,x-1),
                            (y,x-1), (y,x+1),
                            (y+1,x-1), (y+1,x), (y+1, x+1))

        return [(y,x) for y, x in movement_choices if min(y,x) >= 0 and max(y,x) < self.model.env.grid_size and
                 self.passable(self.model.env.grid[y][x].terrain) == True]

    def passable(self, terrain):
        return ((terrain.surface_passable == True and self.surface_movement == True) or
               (terrain.air_passable == True and self.air_movement == True))

class Herbivore (Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

class Carnivore (Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

class Omnivore(Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

class Rabbit (Herbivore):
    def __init__(self, y, x, model, parents = None):
        # re: parents - would we want creature's attributes to be affected by its lineage?  we could if we want.
        Herbivore.__init__(self, y, x, model)
        self.sense_distance = 2

    def take_turn(self, delta_t, step, steps_day):
        response = None
        predators = self.sense_predators()

        # Just hop randomly for the fun of it for testing purposes
        moves = self.possible_movements()
        move_y, move_x = moves[random.randint(0, len(moves)-1)]
        return Move(self, y = move_y, x = move_x)

class Wolf (Carnivore):
    pass

class Hog (Omnivore):
    pass

class Vegitation(Agent):
    def __init__(self, y, x, model):
        Agent.__init__(self, y, x, model)
        self.food_value = 0.0
        self.movement_speed = 1
        self.growth_rate = 1

    def take_turn(self, delta_t, step, steps_day):
        super(Vegitation, self).take_turn(delta_t, step, steps_day)
        return Grow(self, self.growth_rate * delta_t)

class EdiblePlant(Vegitation):
    def __init__(self, y, x, model):
        Vegitation.__init__(self, y, x, model)