"""lists for storing data"""
fellows = []
staff = []
offices = []
living_spaces = []


class Model:
    """ Contains the methods for accessing the storage lists"""

    def __init__(self):
        self.fellows = fellows
        self.staff = staff
        self.offices = offices
        self.living_spaces = living_spaces

    def update(self, item_to_add, list_to_be_appended):
        """ Updates a new item to the selected list"""

        successful = True

        if list_to_be_appended == "fellows":
            self.fellows.append(item_to_add)
            return successful
        elif list_to_be_appended == "staff":
            self.staff.append(item_to_add)
            return successful
        elif list_to_be_appended == "offices":
            self.offices.append(item_to_add)
            return successful
        elif list_to_be_appended == "living_spaces":
            self.living_spaces.append(item_to_add)
            return successful
        else:
            return not successful

    @staticmethod
    def get_list(list_to_be_returned):
        """ Returns the selected list"""

        found = True

        if list_to_be_returned == "fellows":
            return fellows
        elif list_to_be_returned == "staff":
            return staff
        elif list_to_be_returned == "offices":
            return offices
        elif list_to_be_returned == "living_spaces":
            return living_spaces
        else:
            return not found

    @staticmethod
    def get_fellow(fellow_name):
        """ Return a dictionary containing the details of the specified fellow"""
        found = True
        for fellow in fellows:
            if fellow.name == fellow_name:
                return fellow
        return not found

    @staticmethod
    def get_staff(staff_name):
        """ Return a dictionary item containing the details of the specified staff"""
        found = True
        for staff_member in staff:
            if staff_member.name == staff_name:
                return staff_member
        return not found

    @staticmethod
    def get_office(office_name):
        """ Return a dictionary item with the details of the specified office"""
        found = True
        for office in offices:
            if office.name == office_name:
                return office
        return not found

    @staticmethod
    def get_living_space(living_space_name):
        """ Return a dictionary item with the details of the specified living space"""
        found = True
        for living_space in living_spaces:
            if living_space.name == living_space_name:
                return living_space
        return not found

    def flush(self):
        self.fellows.clear()
        self.staff.clear()
        self.offices.clear()
        self.living_spaces.clear()

