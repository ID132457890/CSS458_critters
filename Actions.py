# Basic stubs of how the action classes might possibly work

class Action(object):
    def __init__(self):
        pass

class Attack(Action):
    def __init__(self, other):
        Action.__init__(self, other)
        pass

class Defence(Action):
    pass

class Flee(Defence):
    pass

class Bite(Attack):
    def __init__(self, other):
        Attack.__init__(self, other)
        pass

class Eat(Action):
    pass

class Move(Action):
    pass
