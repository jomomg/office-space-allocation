import random
from models import Model
import room
import person

MAX_OFFICE_CAP = 6
MAX_LIVING_SPACE_CAP = 4


class Dojo:
    """This class contains methods for adding persons, creating new rooms, and for returning
       all rooms or all persons in storage
    """

    def __init__(self):
        """Instantiates the Model class to allow for storage"""
        self.model = Model()

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
                            if office.current_capacity < MAX_OFFICE_CAP]
        if not non_full_offices:
            raise ValueError("There are no offices to allocate")

        if person_type == "fellow":
            random_office = random.choice(non_full_offices)
            fellow = Model.get_fellow(person_name)
            random_office.current_capacity += 1
            fellow.current_office = random_office.name
            return successful

        elif person_type == "staff":
            random_office = random.choice(non_full_offices)
            staff = Model.get_staff(person_name)
            random_office.current_capacity += 1
            staff.current_office = random_office.name
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
                                  if living_space.current_capacity < MAX_LIVING_SPACE_CAP]

        if not non_full_living_spaces:
            raise ValueError("There are no living spaces to allocate")
        random_living_space = random.choice(non_full_living_spaces)
        fellow = Model.get_fellow(fellow_name)
        random_living_space.current_capacity += 1
        fellow.current_living_space = random_living_space.name

        return successful

    def create_new_office(self, name):
        """ Creates a new office """

        successful = True
        new_office = room.Office(name)

        # get the existing offices
        offices = Model.get_list("offices")
        living_spaces = Model.get_list("living_spaces")
        # check whether the office already exists, if it does raise an exception
        similar_office = [office for office in offices if office.name == name]
        similar_living_space = [ls for ls in living_spaces if ls.name == name]
        if similar_office or similar_living_space:
            raise ValueError("An office or living space '{}' already exists".format(name))
        self.model.update(new_office, "offices")
        return successful

    def create_new_living_space(self, name):
        """ Creates a new living space """

        successful = True
        new_living_space = room.LivingSpace(name)
        living_spaces = Model.get_list("living_spaces")
        offices = Model.get_list("offices")
        # check whether the living space already exists, if it does raise an exception
        similar_living_space = [ls for ls in living_spaces if ls.name == name]
        similar_office = [office for office in offices if office.name == name]
        if similar_living_space or similar_office:
            raise ValueError("An office or living space '{}' already exists".format(name))
        # create new living space
        self.model.update(new_living_space, "living_spaces")
        return successful

    def add_fellow(self, name, wants_accommodation=False):
        """ Adds a new fellow """

        new_fellow = person.Fellow(name)
        self.model.update(new_fellow, "fellows")
        print("Fellow {} has been successfully added".format(new_fellow.name))
        try:
            self.allocate_office_space(new_fellow.name, person_type="fellow")
            print("{} has been allocated the office {}"
                  .format(new_fellow.name, new_fellow.current_office))
        except ValueError as e:
                print(e)

        if wants_accommodation:
            try:
                self.allocate_living_space(new_fellow.name)
                print("{} has been allocated the living space {}"
                      .format(new_fellow.name, new_fellow.current_living_space))
            except ValueError as e:
                print(e)

    def add_staff(self, name):
        """ Adds a new member of staff """

        new_staff = person.Staff(name)
        self.model.update(new_staff, "staff")
        print("Staff {} has been successfully added".format(new_staff.name))
        try:
            self.allocate_office_space(new_staff.name, person_type="staff")
            print("{} has been allocated the office {}"
                  .format(new_staff.name, new_staff.current_office))
        except ValueError as e:
            print(e)

    def get_persons_by_room(self, room_name):
        """Return a list of persons in the given room_name"""
        pass

    def get_allocations(self):
        """Return a dictionary with all the allocations as shown
           {room_name: [all persons in the room]}
        """
        pass

    def get_unallocated(self):
        pass

    @property
    def all_fellows(self):
        """ Returns a list containing all the fellows added """
        return Model.get_list("fellows")

    @property
    def all_staff(self):
        """ Returns a list containing all added members of staff"""
        return Model.get_list("staff")

    @property
    def all_offices(self):
        """ Return a list containing all the offices created """

        return Model.get_list("offices")

    @property
    def all_living_spaces(self):
        """ Return a list containing all the living spaces created """
        return Model.get_list("living_spaces")
