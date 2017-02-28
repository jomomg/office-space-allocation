import unittest
from classes import Fellow, Staff, Office, LivingSpace


class RoomTests(unittest.TestCase):
    def setUp(self):
        self.new_office = Office()
        self.new_living_space = LivingSpace()

    def test_create_new_office(self):
        self.new_office.create_new("Test")
        self.assertEqual(self.new_office.all_offices.count("Test"), 1,
                         "A new office was not created")

    def test_create_new_living_space(self):
        self.new_living_space.create_new("Test")
        self.assertEqual(self.new_living_space.all_living_spaces.count("Test"), 1,
                         "A new living space was not created")

    def test_does_not_allow_duplicate_offices(self):
        with self.assertRaises(ValueError):
            self.new_office.create_new("Test")

    def test_does_not_allow_duplicate_living_spaces(self):
        with self.assertRaises(ValueError):
            self.new_living_space.create_new("Test")


class PersonTests(unittest.TestCase):
    def setUp(self):
        self.new_fellow = Fellow()
        self.new_staff = Staff()

    def test_add_new_fellow(self):
        self.new_fellow.add("Harry Potter")
        self.assertEqual(self.new_fellow.all_fellows.count("Harry Potter"), 1,
                         "A new fellow was not added")

    def test_add_new_staff(self):
        self.new_staff.add("Severus Snape")
        self.assertEqual(self.new_staff.all_staff.count("Severus Snape"), 1,
                         "A new staff member was not added")

    def test_does_not_allow_duplicate_fellows(self):
        with self.assertRaises(ValueError):
            self.new_fellow.add("Harry Potter")

    def test_does_not_allow_duplicate_staff(self):
        with self.assertRaises(ValueError):
            self.new_staff.add("Severus Snape")
