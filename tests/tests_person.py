import unittest

from app.dojo import Dojo


class PersonTests(unittest.TestCase):
    """Tests to ensure proper fellow and staff addition

       These tests assume that the 'all_staff' and 'all_fellows' methods return a list.
     """

    def setUp(self):
        self.dojo = Dojo()

    def test_add_new_fellow(self):
        initial_fellow_count = len(self.dojo.all_fellows)
        self.dojo.add_fellow("Harry Potter", "harry@hogwarts.com")
        new_fellow_count = len(self.dojo.all_fellows)
        self.assertEqual(new_fellow_count - initial_fellow_count, 1, "A new fellow was not added")

    def test_add_new_staff(self):
        initial_staff_count = len(self.dojo.all_staff)
        self.dojo.add_staff("Severus Snape", "hbloodprince@hogwarts.com")
        new_staff_count = len(self.dojo.all_staff)
        self.assertEqual(new_staff_count - initial_staff_count, 1, "A new staff member was not added")
