import unittest

from app.dojo import Dojo
from app.models import Model


class RoomTests(unittest.TestCase):
    """Tests to ensure proper living space and office creation

       These tests assume that the 'all_offices' and 'all_living_spaces' methods return a list.
    """

    def setUp(self):
        self.dojo = Dojo()
        self.model = Model()

    def test_create_new_office(self):
        initial_office_count = len(self.dojo.all_offices)
        self.dojo.create_new_office("Test_Office")
        new_office_count = len(self.dojo.all_offices)
        self.assertEqual(new_office_count - initial_office_count, 1,
                         "A new office was not created")

    def test_create_new_living_space(self):
        initial_living_space_count = len(self.dojo.all_living_spaces)
        self.dojo.create_new_living_space("Test_Living_Space")
        new_living_space_count = len(self.dojo.all_living_spaces)
        self.assertEqual(new_living_space_count - initial_living_space_count, 1,
                         "A new living space was not created")

    def test_does_not_allow_duplicate_offices(self):
        with self.assertRaises(ValueError):
            self.dojo.create_new_office("Test")
            self.dojo.create_new_office("Test")

    def test_does_not_allow_duplicate_living_spaces(self):
        with self.assertRaises(ValueError):
            self.dojo.create_new_living_space("Test")
            self.dojo.create_new_living_space("Test")

    def test_allocate_office(self):
        self.dojo.create_new_office("Red")
        self.dojo.add_fellow("Test Fellow")
        self.dojo.add_staff("Test Staff")
        fellow = self.model.get_fellow("Test Fellow")
        staff = self.model.get_staff("Test Staff")
        self.assertEqual((fellow.current_office, staff.current_office), ("Red", "Red"),
                         "Office allocation not successful")
        office_to_check = Model.get_office("Red")
        self.assertEqual(office_to_check.current_capacity, 2,
                         "Office allocation not successful")

    def test_allocate_living_space(self):
        self.dojo.create_new_living_space("Blue")
        self.dojo.add_fellow("Test Fellow 2", wants_accommodation=True)
        fellow = self.model.get_fellow("Test Fellow 2")
        self.assertEqual(fellow.current_living_space, "Blue")
        living_space_to_check = Model.get_living_space("Blue")
        self.assertEqual(living_space_to_check.current_capacity, 1)
