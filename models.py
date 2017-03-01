
fellows = list()
staff = list()
offices = list()
living_spaces = list()


class Model:
    def __init__(self):
        self.fellows = fellows
        self.staff = staff
        self.offices = offices
        self.living_spaces = living_spaces

    def update(self, item_to_add, list_to_be_appended):
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
    def return_list(list_to_be_returned):
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







