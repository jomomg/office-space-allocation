
class Room:
    """This class contains the attributes common to the Office and LivingSpace classes"""

    def __init__(self):
        self.name = None
        self.current_capacity = 0


class Office(Room):
    """Subclass of Room. Contains attributes specific to an office"""

    def __init__(self, office_name):
        Room.__init__(self)
        self.name = office_name


class LivingSpace(Room):
    """Subclass of the Room class. Contains attributes specific to a living space"""

    def __init__(self, living_space_name):
        Room.__init__(self)
        self.name = living_space_name

