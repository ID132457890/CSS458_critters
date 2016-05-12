# Basic stubs of how the action classes might possibly work

class Action(object):
    def __init__(self):
        pass

class Attack(Action):
    def __init__(self, other):
        super()
        pass

class Defence(Action):
    pass

class Flee(Defence):
    pass

class Bite(Attack):
    def __init__(self, other):
        super()
        pass

class Eat(Action):
    pass

class Move(Action):
    pass
