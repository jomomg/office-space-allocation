import random
from models import Model

MAX_OFFICE_CAP = 6
MAX_LIVING_SPACE_CAP = 4


class Room:
    """This class contains the methods and attributes common to the Office and LivingSpace classes"""

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
        all_offices = Model.get_list("offices")
        # return a list of offices with capacity to spare
        non_full_offices = [office
                            for office in all_offices
                            if office["current_capacity"] < MAX_OFFICE_CAP]
        if not non_full_offices:
            raise ValueError("There are no offices to allocate")

        if person_type == "fellow":
            random_office = random.choice(non_full_offices)
            fellow = Model.get_fellow(person_name)
            random_office["current_capacity"] += 1
            fellow["current_office"] = random_office["name"]
            return successful

        elif person_type == "staff":
            random_office = random.choice(non_full_offices)
            staff = Model.get_staff(person_name)
            random_office["current_capacity"] += 1
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
        all_living_spaces = Model.get_list("living_spaces")
        # return a list of living spaces with capacity to spare
        non_full_living_spaces = [living_space
                                  for living_space in all_living_spaces
                                  if living_space["current_capacity"] < MAX_LIVING_SPACE_CAP]

        if not non_full_living_spaces:
            raise ValueError("There are no living spaces to allocate")
        random_living_space = random.choice(non_full_living_spaces)
        fellow = Model.get_fellow(fellow_name)
        random_living_space["current_capacity"] += 1
        fellow["current_living_space"] = random_living_space["name"]

        return successful


class Office(Room):
    """Subclass of Room. Contains methods for creating a new office and returning all offices created"""

    def __init__(self):
        Room.__init__(self)
        self.model = Model()

    def create_new(self, new_office):
        """ Creates a new office """

        successful = True
        self.name = new_office
        new_entry = {"name": self.name, "current_capacity": self.current_capacity}

        # get the existing offices
        offices = Model.get_list("offices")
        # check whether the office already exists, if it does raise an exception
        for entry in offices:
            if entry["name"] == self.name:
                raise ValueError("Office {} already exists".format(self.name))
        self.model.update(new_entry, "offices")
        return successful

    @property
    def all_offices(self):
        """ Return a list containing all the offices created """

        return Model.get_list("offices")


class LivingSpace(Room):
    """Subclass of the Room class. Contains methods for creating a new living space and
       returning all living spaces
    """

    def __init__(self):
        Room.__init__(self)
        self.model = Model()

    def create_new(self, new_living_space):
        """ Creates a new living space """

        successful = True
        self.name = new_living_space
        new_entry = {"name": self.name, "current_capacity": self.current_capacity}

        # get the existing living_spaces
        living_spaces = Model.get_list("living_spaces")
        # check whether the living space already exists, if it does raise an exception
        for entry in living_spaces:
            if entry["name"] == self.name:
                raise ValueError("Living space {} already exists".format(self.name))
        # create new living space
        self.model.update(new_entry, "living_spaces")
        return successful

    @property
    def all_living_spaces(self):
        """ Return a list containing all the living spaces created """
        return Model.get_list("living_spaces")
