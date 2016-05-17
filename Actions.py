import Creature as C
import random

import unittest
# Basic stubs of how the action classes might possibly work

class Action(object):
    def __init__(self):
        pass

    def do_action(self):
        return True

class CombatAction(Action):
    pass

class AttackAction(CombatAction):
    pass

class Bite(AttackAction):
    def __init__(self, agent, other):
        Attack.__init__(self, agent, other)
        pass

class Defence(CombatAction):
    pass

class Flee(Defence):
    pass

class Attack(Action):
    """
    Class that defines the rules of combat and carries out allowing each creature to choose their attack or
    defense strategies.
    """

    def __init__(self, attacker, attacked):
        Action.__init__(self)
        self.attacker = attacker
        self.attacked = attacked

    def combat(self):
        resolved = False
        while not resolved:
            attack = self.attacker.combat_attack(self)
            defense = self.attacked.combat_defense(self)
            initiative_roll = None
            while initiative_roll is None:
                defense_roll = random.randint(1, Creature.max_speed)
                attack_roll = random.randint(1, Creature.max_speed)
                if attack_roll > defense_roll and self.attacker.speed >= attack_roll:
                    # successful attack
                    initiative_roll = attack
                elif self.attacked.speed >= defense_roll:
                    # successful defense
                    initiative_roll = defense
                else:
                    pass    # both failed, roll again
            initiative_roll().do_action()
            if initiative_roll().complete():
                resolved = True
            else:
                if initiative_roll == attack:
                    defense.do_action()
                    if defense().complete():
                        resolved = True
                else:
                    attack.do_action()
                    if attack().complete():
                        resolved = True
        self.attacker.combat_cleanup()      # allow attacker to eat the spoils, etc
        self.attacked.combat_cleanup()      # just in case there's something that should be done after combat

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
        self.agent.model.logger.log(0,"%r ate %r for %f, eater energy now:%f ate energy now %f." %
                    (self.agent, self.other, amount, self.agent.energy, self.other.food_value))
        self.other.be_eaten(self.agent)
        return True

class Drink(Action):
    def __init__(self, agent):
        self.agent = agent

    def do_action(self):
        if self.agent.model.env.water_available(self.agent):
            self.agent.hydration += self.agent.drink_per_day * self.agent.model.delta_t
            #print ("%r drank, h: %f" % (self.agent, self.agent.hydration))
            return True

class NoAction(Action):
    pass

class Grow(Action):
    def __init__(self, agent, amount):
        self.agent = agent
        self.amount = amount

    def do_action(self):
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
    if isinstance(eater, C.Herbivore):
        if isinstance(eaten, C.Vegitation):
            return True
        else:
            return False
    elif isinstance(eater, C.Carnivore):
        if isinstance(eaten, C.Vegitation):
            return False
        else:
            return True
    elif isinstance(eater, C.Omnivore):
        return True
    else:
        return False

class ModelTests(unittest.TestCase):
    def tests(self):
        a = []
        a.append(C.Wolf(x = 0, y = 0, model = None))
        a.append(C.Hog(x = 0, y = 0, model = None))
        a.append(C.Rabbit(x = 0, y = 0, model = None))
        a.append(C.EdiblePlant(x = 0, y = 0, model = None))

        for i in a:
            for j in a:
                print ("%r can eat %r: %r" % (i, j, can_eat(i,j)))


if __name__ == "__main__":
    tests = ModelTests()
    tests.tests()
