from Actions import *
import random

class Agent (object):
    def __init__(self, y, x, model):
        self.location = (y,x)
        self.model = model
        self.PREDATOR = ("Carnivore", "Omnivore")
        self.PLANTS = ("Vegitation")

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
        self.hydration = 5.0
        self.energy = 5.0
        self.daily_hydration_usage = 0.3
        self.daily_energy_usage = 0.3
        self.health = 1.0
        self.food_value = 1.0
        self.alive = True
        self.hunger = 3.0
        self.thirst = 3.0
        self.eat_per_day = 4
        self.drink_per_day = 4

    def take_turn(self, delta_t, step, steps_day):
        return super(Creature, self).take_turn(delta_t, step, steps_day)

    def daily_agent_maintenance(self):
        if self.alive == True:
            self.energy -= self.daily_energy_usage
            self.hydration -= self.daily_hydration_usage
            if min(self.energy, self.hydration) <= 0:
                self.model.logger.log(0, "%r died e %f h %f" % (self, self.energy, self.hydration))
                self.alive = False
                self.movement_speed = 0
        else:
            self.food_value -= .5
            if self.food_value <= 0:
                self.model.env.remove_agent(self)
                self.model.logger.log(0, "%r rotted away" % self)

    def sense_agents(self, search_for = (Agent,), distance = 0):
        search_list = [self.location]
        if distance > 0:
            search_list.extend(self.model.env.neighbor_locations(self, distance))
        result_grid_points = [self.model.env.grid[y][x] for y, x in search_list]
        agents_found = []
        for gp in result_grid_points:
            for agent in gp.agents:
                for z in search_for:
                    if isinstance(agent, z) == True:
                        agents_found.append(agent)
                        break

        return agents_found

    def possible_movements(self):
        movement_choices = self.model.env.neighbor_locations(agent=self)
        return [(y,x) for y, x in movement_choices if self.passable(self.model.env.grid[y][x].terrain) == True]

    def passable(self, terrain):
        return ((terrain.surface_passable == True and self.surface_movement == True) or
               (terrain.air_passable == True and self.air_movement == True))

    def consume(self, search_for):
        if self.energy < self.hunger:
            food = self.sense_agents(search_for = search_for)
            if len(food):
                return Eat(self, food[0])
        if self.hydration < self.thirst:
            if self.model.env.water_available(self):
                return Drink(self)
        return None

class Herbivore (Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

    def consume(self):
        return super(Herbivore, self).consume(search_for = (Vegitation,))

class Carnivore (Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

    def consume(self):
        return super(Carnivore, self).consume(search_for=(Creature,))

class Omnivore(Creature):
    def __init__(self, y, x, model):
        Creature.__init__(self, y, x, model)

    def consume(self):
        return super(Omnivore, self).consume(search_for=(Vegitation,Creature))

class Rabbit (Herbivore):
    def __init__(self, y, x, model, parents = None):
        # re: parents - would we want creature's attributes to be affected by its lineage?  we could if we want.
        Herbivore.__init__(self, y, x, model)
        self.sense_distance = 2

    def take_turn(self, delta_t, step, steps_day):
        # eat/drink if needed
        move = self.consume()
        if move is None:
            # Just hop randomly for the fun of it for testing purposes
            moves = self.possible_movements()
            move_y, move_x = moves[random.randint(0, len(moves) - 1)]
            return Move(self, y=move_y, x=move_x)
        else:
            return move

class Wolf (Carnivore):
    pass

class Hog (Omnivore):
    pass

class Vegitation(Agent):
    def __init__(self, y, x, model):
        Agent.__init__(self, y, x, model)
        self.food_value = 0.0
        self.movement_speed = 1
        self.growth_rate = 5.5

    def take_turn(self, delta_t, step, steps_day):
        super(Vegitation, self).take_turn(delta_t, step, steps_day)
        return Grow(self, self.growth_rate * delta_t)

class EdiblePlant(Vegitation):
    def __init__(self, y, x, model):
        Vegitation.__init__(self, y, x, model)