class Terrain(object):
    def __init__(self):
        self.water_available = False
        self.surface_passable = False
        self.air_passable = False

class Grasslands(Terrain):
    def __init__(self):
        super()
        self.surface_passable = True
        self.air_passable = True

class Wetlands (Terrain):
    def __init__(self):
        super()
        self.surface_passable = True
        self.air_passable = True
        self.water_available = True