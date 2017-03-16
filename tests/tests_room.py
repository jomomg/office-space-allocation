import unittest
import os

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
        self.dojo.create_new_office("Test")
        with self.assertRaises(ValueError):
            self.dojo.create_new_office("Test")

    def test_does_not_allow_duplicate_living_spaces(self):
        self.dojo.create_new_living_space("Test")
        with self.assertRaises(ValueError):
            self.dojo.create_new_living_space("Test")

    def test_allocate_office(self):
        self.dojo.create_new_office("Red")
        self.dojo.add_fellow("Test Fellow", "fellow@fellow.com")
        self.dojo.add_staff("Test Staff", "staff@staff.com")
        fellow = self.model.get_fellow("Test Fellow", "fellow@fellow.com")
        staff = self.model.get_staff("Test Staff", "staff@staff.com")
        self.assertEqual((fellow.current_office, staff.current_office), ("Red", "Red"),
                         "Office allocation not successful")
        office_to_check = Model.get_office("Red")
        self.assertEqual(office_to_check.current_capacity, 2,
                         "Office allocation not successful")

    def test_allocate_living_space(self):
        self.dojo.create_new_living_space("Blue")
        self.dojo.add_fellow("Test Fellow 2","test@test.com",  wants_accommodation=True)
        fellow = self.model.get_fellow("Test Fellow 2", "test@test.com")
        self.assertEqual(fellow.current_living_space, "Blue")
        living_space_to_check = Model.get_living_space("Blue")
        self.assertEqual(living_space_to_check.current_capacity, 1)

    # Reallocation tests

    def test_reallocation_successful(self):
        self.model.flush()
        old_office_name = "Blue"
        new_office_name = "Red"
        self.dojo.create_new_office(old_office_name)
        self.dojo.add_fellow("John", "john@john.com")
        self.dojo.create_new_office(new_office_name)
        self.dojo.reallocate_person("John", "Red")
        new_fellow = self.model.get_fellow("John", "john@john.com")
        msg = "person was not successfully reallocated"
        self.assertEqual(new_office_name, new_fellow.current_office, msg)

    def test_raises_exception_if_person_not_found(self):
        self.model.flush()
        self.dojo.create_new_office("Green")
        with self.assertRaises(ValueError):
            self.dojo.reallocate_person("Phillip", "Green")

    def test_raises_exception_if_destination_room_is_full(self):
        self.model.flush()
        self.dojo.create_new_office("Yellow")
        new_fellows = ["Mary", "Monica", "Lisa", "Lucy", "Jane", "Jennifer"]
        for fellow in new_fellows:
            self.dojo.add_fellow(fellow, fellow + "@dojo.com")
        with self.assertRaises(OverflowError):
            self.dojo.reallocate_person("Julia", "Yellow")

    def test_cannot_reallocate_staff_to_living_space(self):
        self.model.flush()
        self.dojo.create_new_office("Orange")
        self.dojo.create_new_living_space("Delta")
        self.dojo.add_staff("James", "james@james.com")
        with self.assertRaises(ValueError):
             self.dojo.reallocate_person("James", "Delta")

    def test_raises_exception_if_destination_room_is_non_existent(self):
        self.model.flush()
        self.dojo.create_new_office("Violet")
        self.dojo.add_fellow("David", "david@david.com")
        with self.assertRaises(ValueError):
            self.dojo.reallocate_person("David", "Cyan")

    def test_loads_people_from_txt_file(self):
        self.model.flush()
        self.dojo.create_new_office("Iota")
        self.dojo.create_new_living_space("Zeta")
        with open("people.txt", "w") as test_file:
            output = "BRUCE WAYNE FELLOW Y\n" \
                     "BARRY ALLEN STAFF\n"
            test_file.write(output)

        self.dojo.load_people_from_txt_file("people")
        new_fellow = self.model.get_fellow("Bruce Wayne", "bruce@gotham.com")
        new_staff = self.model.get_staff("Barry Allen", "allen@nationalcity.com")
        self.assertTrue(new_fellow)
        self.assertTrue(new_staff)
        self.assertEqual("Iota", new_staff.current_office)
        self.assertEqual("Zeta", new_fellow.current_living_space)
        os.remove("people.txt")

    def test_raises_exception_if_txt_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.dojo.load_people_from_txt_file("test_file.txt")
