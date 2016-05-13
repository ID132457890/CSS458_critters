import Creature

import unittest
# Basic stubs of how the action classes might possibly work

class Action(object):
    def __init__(self):
        pass

    def do_action(self):
        return True

class Attack(Action):
    def __init__(self, other):
        Action.__init__(self, other)
        pass

class Defence(Action):
    pass

class Flee(Defence):
    pass

class Bite(Attack):
    def __init__(self, agent, other):
        Attack.__init__(self, agent, other)
        pass

class Eat(Action):
    def __init__(self, agent, other):
        if not can_eat(agent, other):
            raise Exception ("Invalid consumption! %s cannot consume %s" % (agent, other))
        else:
            self.agent = agent
            self.other = other

    def do_action(self):
        amount = self.agent.eat_per_day * self.agent.model.delta_t
        amount = min(amount, self.other.food_value)
        self.agent.energy += amount
        self.other.food_value -= amount
        print ("%r ate %r for %f" % (self.agent, self.other, amount))
        return True


class NoAction(Action):
    pass

class Grow(Action):
    def __init__(self, agent, amount):
        self.agent = agent
        self.amount = amount

    def do_action(self):
        rate = self.agent.growth_rate
        self.agent.food_value += self.amount
        return True

class Move(Action):
    def __init__(self, agent, y, x):
        self.move_y = y
        self.move_x = x
        self.agent = agent

    def do_action(self):
        #print ("%s moving to %d, %d from %d, %d" % (self.agent, self.move_y,self.move_x, self.agent.location[0], self.agent.location[1]))
        model = self.agent.model
        old_location = model.env.grid[self.agent.location[0]][self.agent.location[1]]
        new_location = model.env.grid[self.move_y][self.move_x]
        old_location.agents.remove(self.agent)
        new_location.agents.append(self.agent)
        self.agent.location = (self.move_y, self.move_x)
        return True

def can_eat(eater, eaten):
    if isinstance(eater, Creature.Herbivore):
        if isinstance(eaten, Creature.Vegitation):
            return True
        else:
            return False
    elif isinstance(eater, Creature.Carnivore):
        if isinstance(eaten, Creature.Vegitation):
            return False
        else:
            return True
    elif isinstance(eater, Creature.Omnivore):
        return True
    else:
        return False

class ModelTests(unittest.TestCase):
    def tests(self):
        a = []
        a.append(Wolf(x = 0, y = 0, model = None))
        a.append(Hog(x = 0, y = 0, model = None))
        a.append(Rabbit(x = 0, y = 0, model = None))
        a.append(EdiblePlant(x = 0, y = 0, model = None))

        for i in a:
            for j in a:
                print ("%r can eat %r: %r" % (i, j, can_eat(i,j)))


if __name__ == "__main__":
    tests = ModelTests()
    tests.tests()
