import unittest
from person import Fellow, Staff
from dojo import Dojo
from models import Model


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


class PersonTests(unittest.TestCase):
    """Tests to ensure proper fellow and staff addition

       These tests assume that the 'all_staff' and 'all_fellows' methods return a list.
     """

    def setUp(self):
        self.dojo = Dojo()

    def test_add_new_fellow(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow("Harry Potter")
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1, "A new fellow was not added")

    def test_add_new_staff(self):
        initial_staff_count = len(self.dojo.all_staff)
        self.dojo.add_staff("Severus Snape")
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1, "A new staff member was not added")

    def test_print_room_occupants(self):
        pass


class PrintTests(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_get_occupants_of_given_room(self):
        self.dojo.create_new_living_space("Chui")
        self.dojo.create_new_office("Simba")
        persons = ["Harry Potter", "Hermione Granger", "Ron Weasley", "Draco Malfoy"]
        for person in persons:
            self.dojo.add_fellow(person, wants_accommodation=True)
        persons_in_living_space = self.dojo.get_persons_by_room(room_name="Chui")
        persons_in_office = self.dojo.get_persons_by_room(room_name="Simba")
        msg = "Could not get the occupants of the given room"
        self.assertEqual(persons_in_living_space, persons, msg)
        self.assertEqual(persons_in_office, persons, msg)

    def test_get_all_room_allocations(self):
        self.dojo.create_new_living_space("Living Space 1")
        self.dojo.create_new_office("Office 1")
        persons = ["Mary", "John", "Tom", "Harry"]
        expected_allocations = {"Living Space 1": persons, "Office 1": persons}
        for person in persons:
            self.dojo.add_fellow(person, wants_accommodation=True)
        actual_allocations = self.dojo.get_allocations()
        self.assertEqual(expected_allocations, actual_allocations, "The wrong allocations were returned")

    def test_print_unallocated_persons(self):
        persons = ["Alpha", "Beta", "Gamma", "Delta"]
        for person in persons:
            self.dojo.add_fellow(person, wants_accommodation=True)
        unallocated_persons = self.dojo.get_unallocated()
        msg = "Could not get the unallocated people"
        self.assertEqual(unallocated_persons, persons)




