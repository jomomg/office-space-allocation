from models import Model


class Dojo:
    def __init__(self):
        pass


class Person:
    def __init__(self):
        pass


class Fellow(Person):
    def __init__(self):
        Person.__init__(self)
        self.model = Model()

    def add(self, new_fellow):
        """ Adds a new fellow """

        if not isinstance(new_fellow, str):
            raise TypeError("Input is not a string")
        self.model.update(new_fellow, list_to_be_appended="fellows")

    @property
    def all_fellows(self):
        """ Returns a list containing all the fellows added """

        return Model.return_list(list_to_be_returned="fellows")


class Staff(Person):
    def __init__(self):
        Person.__init__(self)
        self.model = Model()

    def add(self, new_staff):
        """ Adds a new member of staff """

        if not isinstance(new_staff, str):
            raise TypeError("Input is not a string")
        self.model.update(new_staff, list_to_be_appended="staff")

    @property
    def all_staff(self):
        """ Returns a list containing all added members of staff """

        return Model.return_list(list_to_be_returned="staff")


class Office(Dojo):
    def __init__(self):
        Dojo.__init__(self)
        self.model = Model()

    def create_new(self, new_office):
        """ Creates a new office """

        if not isinstance(new_office, str):
            raise TypeError("Input is not a string")
        offices = Model.return_list(list_to_be_returned="offices")

        # check whether the office already exists, if it does raise an exception
        if offices.count(new_office) == 1:
            raise ValueError("Office already exists")
        self.model.update(new_office, list_to_be_appended="offices")

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

        living_spaces = Model.return_list(list_to_be_returned="living_spaces")

        # check whether the living space already exists, if it does raise an exception
        if living_spaces.count(new_living_space) == 1:
            raise ValueError("Living space already exists")
        # create new living space
        self.model.update(new_living_space, list_to_be_appended="living_spaces")

    @property
    def all_living_spaces(self):
        """ Return a list containing all the living spaces created """

        return Model.return_list(list_to_be_returned="living_spaces")

