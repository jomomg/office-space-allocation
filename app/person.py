
class Person:
    """This class contains the attributes common to the Fellow and Staff classes"""

    def __init__(self):
        self.name = None
        self.current_office = None
        self.current_living_space = None


class Fellow(Person):
    """This class contains the attributes unique to a fellow"""
    def __init__(self, name):
        Person.__init__(self)
        self.name = name
        self.current_office = None



class Staff(Person):
    """This class contains the attributes unique to a staff member"""
    def __init__(self, name):
        Person.__init__(self)
        self.name = name
        self.current_office = None
