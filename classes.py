from models import Model
import random

MAX_OFFICE_CAP = 6
MAX_LIVING_SPACE_CAP = 4


class Dojo:
    def __init__(self):
        self.name = None
        self.current_capacity = 0

    @staticmethod
    def allocate_office_space(person_name, person_type):
        """ This methods randomly allocates an office to a fellow or staff.

            Returns True if successful and False if not
        """

        successful = True
        random.seed()

        # return the list of available offices
        offices = Model.return_list(list_to_be_returned="offices")
        # return a list of offices with capacity to spare
        non_full_offices = [x for x in offices if x["current_capacity"] < MAX_OFFICE_CAP]
        if not non_full_offices:
            raise ValueError("There are no offices to allocate")

        if person_type == "fellow":
            # get a random office from the list of non full offices
            random_office = random.choice(non_full_offices)
            # get the fellow with the given name
            fellow = Model.get_fellow(person_name)
            # increment the current capacity of the chosen office by 1
            random_office["current_capacity"] += 1
            # add the office name to be the fellow's current office
            fellow["current_office"] = random_office["name"]
            return successful

        elif person_type == "staff":
            # get a random office from the list of non full offices
            random_office = random.choice(non_full_offices)
            # get the staff member with the given name
            staff = Model.get_staff(person_name)
            # increment the current capacity of the chosen office by 1
            random_office["current_capacity"] += 1
            # add the office name to be the staff member's current office
            staff["current_office"] = random_office["name"]
            return successful

        else:
            return not successful

    @staticmethod
    def allocate_living_space(fellow_name):
        """ This methods randomly allocates a living space to a fellow or staff.

            Returns True if successful and False if not
        """

        successful = True
        random.seed()

        # return a list of available living spaces
        living_spaces = Model.return_list(list_to_be_returned="living_spaces")
        # return a list of living spaces with capacity to spare
        non_full_living_spaces = [x for x in living_spaces if x["current_capacity"] < MAX_LIVING_SPACE_CAP]

        if not non_full_living_spaces:
            raise ValueError("There are no living spaces to allocate")
        # get a random living space
        random_living_space = random.choice(non_full_living_spaces)
        # get the fellow specified
        fellow = Model.get_fellow(fellow_name)
        # increment the current capacity of the living space by 1
        random_living_space["current_capacity"] += 1
        # add the living space's name to the fellows current living space
        fellow["current_living_space"] = random_living_space["name"]

        return successful


class Person:
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

        if not isinstance(new_fellow, str):
            raise TypeError("Input is not a string")

        self.name = new_fellow
        new_entry = {"name": self.name,
                     "current_office": self.current_office,
                     "current_living_space": self.current_living_space}

        self.model.update(new_entry, list_to_be_appended="fellows")

    @property
    def all_fellows(self):
        """ Returns a list containing all the fellows added """

        return Model.return_list(list_to_be_returned="fellows")

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

        if not isinstance(new_staff, str):
            raise TypeError("Input is not a string")

        self.name = new_staff
        new_entry = {"name": self.name, "current_office": self.current_office}
        self.model.update(new_entry, list_to_be_appended="staff")

    @property
    def all_staff(self):
        """ Returns a list containing all added members of staff"""

        return Model.return_list(list_to_be_returned="staff")


class Office(Dojo):
    def __init__(self):
        Dojo.__init__(self)
        self.model = Model()

    def create_new(self, new_office):
        """ Creates a new office """

        successful = True
        if not isinstance(new_office, str):
            raise TypeError("Input is not a string")

        self.name = new_office
        new_entry = {"name": self.name, "current_capacity": self.current_capacity}

        # get the existing offices
        offices = Model.return_list(list_to_be_returned="offices")
        # check whether the office already exists, if it does raise an exception
        for entry in offices:
            if entry["name"] == self.name:
                raise ValueError("Office already exists")
        self.model.update(new_entry, list_to_be_appended="offices")
        return successful

    @property
    def all_offices(self):
        """ Return a list containing all the offices created """

        return Model.return_list(list_to_be_returned="offices")


class LivingSpace(Dojo):
    def __init__(self):
        Dojo.__init__(self)
        self.model = Model()

    def create_new(self, new_living_space):
        """ Creates a new living space """

        successful = True
        self.name = new_living_space
        new_entry = {"name": self.name, "current_capacity": self.current_capacity}

        # get the existing living_spaces
        living_spaces = Model.return_list(list_to_be_returned="living_spaces")
        # check whether the living space already exists, if it does raise an exception
        for entry in living_spaces:
            if entry["name"] == self.name:
                raise ValueError("Living space already exists")
        # create new living space
        self.model.update(new_entry, list_to_be_appended="living_spaces")
        return successful

    @property
    def all_living_spaces(self):
        """ Return a list containing all the living spaces created """

        return Model.return_list(list_to_be_returned="living_spaces")



