import unittest
from person import Fellow, Staff
from dojo import Office, LivingSpace
from models import Model


class RoomTests(unittest.TestCase):
    """Tests to ensure proper living space and office creation

       These tests assume that the 'all_offices' and 'all_living_spaces' methods return a list.
    """

    def setUp(self):
        self.new_office = Office()
        self.new_living_space = LivingSpace()
        self.new_fellow = Fellow()
        self.new_staff = Staff()

    def test_create_new_office(self):
        initial_office_count = len(self.new_office.all_offices)
        self.new_office.create_new("Test")
        new_office_count = len(self.new_office.all_offices)
        self.assertEqual(new_office_count - initial_office_count, 1,
                         "A new office was not created")

    def test_create_new_living_space(self):
        initial_living_space_count = len(self.new_living_space.all_living_spaces)
        self.new_living_space.create_new("Test")
        new_living_space_count = len(self.new_living_space.all_living_spaces)
        self.assertEqual(new_living_space_count - initial_living_space_count, 1,
                         "A new living space was not created")

    def test_does_not_allow_duplicate_offices(self):
        with self.assertRaises(ValueError):
            self.new_office.create_new("Test")

    def test_does_not_allow_duplicate_living_spaces(self):
        with self.assertRaises(ValueError):
            self.new_living_space.create_new("Test")

    def test_allocate_office(self):
        # add a new fellow and a new staff member
        self.new_fellow.add("Test Fellow")
        self.new_staff.add("Test Staff")
        # create a new office
        self.new_office.create_new("Red")
        # allocate them an office space
        self.new_office.allocate_office_space("Test Fellow", "fellow")
        self.new_office.allocate_office_space("Test Staff", "staff")
        # get the office they have been allocated
        fellow_office = self.new_fellow.get_current_office("Test Fellow", "fellow")
        staff_office = self.new_staff.get_current_office("Test Staff", "staff")
        # check if it is the correct living space
        self.assertEqual((fellow_office, staff_office), ("Red", "Red"),
                         "Office allocation not successful")
        # check if the office capacity is correct
        office_to_check = Model.get_office("Red")
        self.assertEqual(office_to_check["current_capacity"], 2,
                         "Office allocation not successful")

    def test_allocate_living_space(self):
        # add a new fellow
        self.new_fellow.add("Test Fellow 2")
        # create a new living space
        self.new_living_space.create_new("Blue")
        # allocate the fellow a living space
        self.new_living_space.allocate_living_space("Test Fellow 2")
        # get the living space the fellow has been allocated
        living_space_alloc = self.new_fellow.get_current_living_space("Test Fellow 2")
        # check whether it is the correct living space
        self.assertEqual(living_space_alloc, "Blue")
        # check whether the capacity is correct
        living_space_to_check = Model.get_living_space("Blue")
        self.assertEqual(living_space_to_check["current_capacity"], 1)


class PersonTests(unittest.TestCase):
    """Tests to ensure proper fellow and staff addition

       These tests assume that the 'all_staff' and 'all_fellows' methods return a list.
     """

    def setUp(self):
        self.new_fellow = Fellow()
        self.new_staff = Staff()

    def test_add_new_fellow(self):
        initial_fellow_count = len(self.new_fellow.all_fellows)
        self.new_fellow.add("Harry Potter")
        new_fellow_count = len(self.new_fellow.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1,
                         "A new fellow was not added")

    def test_add_new_staff(self):
        initial_staff_count = len(self.new_staff.all_staff)
        self.new_staff.add("Severus Snape")
        new_staff_count = len(self.new_staff.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1,
                         "A new staff member was not added")

