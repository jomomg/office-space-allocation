class Dojo:
    pass


class Person:
    pass


class Fellow(Person):
    def __init__(self):
        pass

    def add(self, new_fellow):
        pass

    @property
    def all_fellows(self):
        return []


class Staff(Person):
    def __init__(self):
        pass

    def add(self, new_fellow):
        pass

    @property
    def all_staff(self):
        return []


class Office(Dojo):
    def __init__(self):
        pass

    def create_new(self, new_office):
        pass

    @property
    def all_offices(self):
        return []


class LivingSpace(Dojo):
    def __init__(self):
        pass

    def create_new(self, new_living_space):
        pass

    @property
    def all_living_spaces(self):
        return []

