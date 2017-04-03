import os
import unittest

from app.dojo import Dojo
from app.models import Model


class PrintTests(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.model = Model()

    def test_raises_error_on_non_existent_room(self):
        expected_response = "The room you specified was not found"
        actual_response = self.dojo.print_persons_by_room("Nonexistent")
        self.assertEqual(expected_response, actual_response)

    def test_print_occupants_of_given_living_space(self):
        self.model.flush()
        self.dojo.create_new_living_space("Chui")
        person = "Harry"
        self.dojo.add_fellow(person, person + "@dojo.com", wants_accommodation=True)
        persons_in_living_space = self.dojo.print_persons_by_room(room="Chui")
        expected_output = "(LIVING SPACE) CHUI:\n" \
                          "Harry@dojo.com Harry"
        msg = "Could not get the occupants of the given room"
        self.assertEqual(expected_output, persons_in_living_space, msg)

    def test_print_occupants_of_given_office(self):
        self.model.flush()
        self.dojo.create_new_office("Simba")
        person = "Hermione"
        self.dojo.add_fellow(person, person + "@dojo.com")
        persons_in_office = self.dojo.print_persons_by_room(room="Simba")
        expected_output = "(OFFICE) SIMBA:\n" \
                          "Hermione@dojo.com Hermione"
        msg = "Could not get the occupants of the given room"
        self.assertEqual(expected_output, persons_in_office, msg)

    def test_prints_all_room_allocations(self):
        self.model.flush()
        self.dojo.create_new_living_space("Alpha")
        self.dojo.create_new_office("Orange")
        person = "Mary"
        l_space_allocations = "(L_SPACE) ALPHA:\n" \
                              "-----------------------------\n" + \
                              "Mary@dojo.com Mary\n"
        office_allocations = "(OFFICE) ORANGE:\n" + \
                             "-----------------------------\n" + \
                             "Mary@dojo.com Mary\n"
        self.dojo.add_fellow(person, person + "@dojo.com", wants_accommodation=True)
        actual_allocations = self.dojo.print_allocations()
        msg = "The wrong allocations were returned"
        self.assertIn(l_space_allocations, actual_allocations, msg)
        self.assertIn(office_allocations, actual_allocations, msg)

    def test_prints_room_allocations_to_txt_file(self):
        self.model.flush()
        persons = ["James", "Jerry", "Julia", "Jane"]
        self.dojo.create_new_office("Green")
        for person in persons:
            self.dojo.add_fellow(person, person + "@dojo.com")
        self.dojo.print_allocations("room_allocations")
        # make sure the text file has been created
        self.assertTrue(os.path.isfile("room_allocations.txt"))
        expected_output = "OFFICE: GREEN\n" + \
                          "----------------------------\n" + \
                          "JAMES@DOJO.COM JAMES, JERRY@DOJO.COM JERRY, JULIA@DOJO.COM JULIA, JANE@DOJO.COM JANE\n\n"
        with open("room_allocations.txt", "r") as file:
            actual_output = file.read()

        msg = "Information incorrectly printed to file"
        self.assertEqual(expected_output, actual_output, msg)
        os.remove("room_allocations.txt")

    def test_print_unallocated_persons(self):
        self.model.flush()
        persons = "Alpha,Beta,Gamma,Delta"
        for person in persons.split(","):
            self.dojo.add_fellow(person, person+"@dojo.com", wants_accommodation=True)
        unallocated_persons = self.dojo.print_unallocated()
        expected_output = "STAFF WITHOUT AN OFFICE:\n" \
                          "----------------------------\n" \
                          "NO UNALLOCATED STAFF\n\n"  \
                          "FELLOWS WITHOUT AN OFFICE:\n" \
                          "-----------------------------\n"  \
                          "ALPHA, BETA, GAMMA, DELTA\n\n"  \
                          "FELLOWS WITHOUT A LIVING SPACE:\n" \
                          "------------------------------\n"  \
                          "ALPHA, BETA, GAMMA, DELTA\n\n"
        msg = "Could not get the unallocated people"
        self.assertEqual(unallocated_persons, expected_output, msg)

    def test_prints_unallocated_persons_to_txt_file(self):
        self.model.flush()
        fellows = ["Odin", "Thor"]
        for fellow in fellows:
            self.dojo.add_fellow(fellow, fellow + "@dojo.com")
        self.dojo.add_staff("Loki", "loki@dojo.com")
        self.dojo.print_unallocated("unallocated_persons")
        self.assertTrue(os.path.isfile("unallocated_persons.txt"))
        expected_output = "STAFF WITHOUT AN OFFICE:\n" \
                          "----------------------------\n" \
                          "LOKI\n\n"  \
                          "FELLOWS WITHOUT AN OFFICE:\n" \
                          "-----------------------------\n"  \
                          "ODIN, THOR\n\n"  \
                          "FELLOWS WITHOUT A LIVING SPACE:\n" \
                          "------------------------------\n"  \
                          "ODIN, THOR\n\n"
        with open("unallocated_persons.txt", "r") as file:
            actual_output = file.read()

        msg = "Information incorrectly printed to file"
        self.assertEqual(expected_output, actual_output, msg)
        os.remove("unallocated_persons.txt")
        self.model.flush()
