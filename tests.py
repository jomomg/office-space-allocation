import unittest
from classes import Fellow, Staff, Office, LivingSpace


class RoomTests(unittest.TestCase):
    """Tests to ensure proper living space and office creation

       These tests assume that the 'all_offices' and 'all_living_spaces' methods return a list.
       Hence the 'count' method of the list object is used to test
       Whether a new office  or a new living space exists in the list returned.
    """

    def setUp(self):
        self.new_office = Office()
        self.new_living_space = LivingSpace()

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

    def test_only_accepts_string_input(self):
        with self.assertRaises(TypeError):
            self.new_living_space.create_new(12345)
            self.new_office.create_new(12345)


class PersonTests(unittest.TestCase):
    """Tests to ensure proper fellow and staff addition

       These tests assume that the 'all_staff' and 'all_fellows' methods return a list.
       Hence the 'count' method of the list object is used to test
       Whether a new fellow  or a new staff member exists in the list returned.
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

    def test_only_accepts_string_input(self):
        with self.assertRaises(TypeError):
            self.new_fellow.add(12345)
            self.new_staff.add(12345)
