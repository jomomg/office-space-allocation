import unittest
import os

from app.dojo import Dojo
from app.models import Model


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.model = Model()

    def test_save_state_and_load_state(self):
        self.model.flush()
        self.dojo.create_new_office("Blue")
        self.dojo.create_new_living_space("Red")
        self.dojo.add_fellow("Peter", "peter@dojo.com", wants_accommodation=True)
        self.dojo.add_staff("Paul", "paul@dojo.com")

        self.dojo.save_state()  # save data in lists to database
        self.model.flush()  # clear data from storage lists
        self.dojo.load_state("default")  # load data from database to lists

        office = self.model.get_office("Blue")
        living_space = self.model.get_living_space("Red")
        fellow = self.model.get_fellow("Peter", "peter@dojo.com")
        staff = self.model.get_staff("Paul", "paul@dojo.com")

        msg = "State was not successfully saved"
        self.assertEqual(("Blue", "Red"), (office.name, living_space.name), msg)
        self.assertEqual(("Peter", "Paul"), (fellow.name, staff.name), msg)
        os.remove("default.db")

    def test_successfully_creates_and_loads_from_user_supplied_db_file(self):
        self.model.flush()
        self.dojo.create_new_office("Cyan")
        self.dojo.add_fellow("Abel", "abel@dojo.com")

        self.dojo.save_state("test_db")
        self.model.flush()
        self.dojo.load_state("test_db")

        fellow = self.model.get_fellow("Abel", "abel@dojo.com")
        office = self.model.get_office("Cyan")
        self.assertEqual("Abel", fellow.name)
        self.assertEqual("Cyan", office.name)
        os.remove("test_db.db")

    def test_raises_error_if_specified_database_file_is_nonexistent(self):
        self.model.flush()
        self.dojo.add_fellow("Thomas", "thomas@dojo.com")

        self.dojo.save_state()
        self.model.flush()
        actual_err_msg = self.dojo.load_state("non_existent_db")
        expected_err_msg = "The specified database does not exist"
        self.assertEqual(expected_err_msg, actual_err_msg)
