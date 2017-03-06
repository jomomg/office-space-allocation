from models import Model


class Person:
    """This class contains the methods and attributes common to the Fellow and Staff classes"""

    def __init__(self):
        self.name = None
        self.current_office = None

    def get_current_office(self, person_name, person_type):
        """ Returns the current office of the specified person"""

        if person_type == "fellow":
            fellow = Model.get_fellow(person_name)
            self.current_office = fellow["current_office"]
            return self.current_office

        elif person_type == "staff":
            staff = Model.get_staff(person_name)
            self.current_office = staff["current_office"]
            return self.current_office


class Fellow(Person):
    def __init__(self):
        Person.__init__(self)
        self.model = Model()
        self.current_living_space = None

    def add(self, new_fellow):
        """ Adds a new fellow """

        self.name = new_fellow
        # store the new fellow as a dictionary entry
        new_entry = {"name": self.name,
                     "current_office": self.current_office,
                     "current_living_space": self.current_living_space}
        # append the new entry to the fellows list
        self.model.update(new_entry, "fellows")

    @property
    def all_fellows(self):
        """ Returns a list containing all the fellows added """
        return Model.get_list("fellows")

    def get_current_living_space(self, fellow_name):
        """ Returns the current living space of the specified fellow"""

        fellow = Model.get_fellow(fellow_name)
        self.current_living_space = fellow["current_living_space"]
        return self.current_living_space


class Staff(Person):
    def __init__(self):
        Person.__init__(self)
        self.model = Model()
        self.name = None
        self.current_office = None

    def add(self, new_staff):
        """ Adds a new member of staff """

        self.name = new_staff
        # store the new staff member as a dictionary entry
        new_entry = {"name": self.name, "current_office": self.current_office}
        # append the new entry to the staff list
        self.model.update(new_entry, "staff")

    @property
    def all_staff(self):
        """ Returns a list containing all added members of staff"""
        return Model.get_list("staff")
