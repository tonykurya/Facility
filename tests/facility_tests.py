from unittest import TestCase
from .. app.facility import Facility
from .. app.room import Office, LivingSpace
from .. app.person import Manager

import os
import sys
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class TestFacility(TestCase):

    def setUp(self):
        self.facility = Facility()

    def test_create_room(self):
        """
        This method creates rooms of the given type.
        """
        self.assertEqual(self.facility.create_room(
            "Dojo", "office"), "Office {} created successfully.".format(
            "Dojo"))
        self.assertEqual(self.facility.create_room(
            "Emeli", "living_space"),
            "LivingSpace {} created successfully.".format(
            "Emeli"))

    def test_create_room_duplicates(self):
        """
        This method tests that there are no room duplicates.
        """
        self.facility.create_room("DevLab", "office")
        self.assertEqual(self.facility.create_room(
            "DevLab", "office"), "{} is already created.".format(
            "DevLab"))
        self.facility.create_room("Lounge", "living_space")
        self.assertEqual(self.facility.create_room(
            "Lounge", "living_space"), "{} is already created.".format(
            "Lounge"))

    def test_invalid_room_type(self):
        """
        This method tests that an invalid room type.
        """
        self.assertEqual(self.facility.create_room(
            "Dojo", "open_office"), "Invalid room type.")

    def test_add_person(self):
        """
        This method tests that a person \
        can be added successfully to the system.
        """
        self.facility.create_room('Dojo', "office")
        self.assertEqual(self.facility.add_person(
            'Toni Kurya', 'Staff', 'N'),
            "{} a {} added successfully.".format(
            "Toni Kurya", "Staff"))

    def test_add_person_duplicate(self):
        """
        This method tests duplicate additions to the system.
        """
        self.facility.create_room("Dojo", "office")
        self.facility.add_person('Toni Kurya', 'Staff', 'N')
        self.assertEqual(self.facility.add_person(
            'Toni Kurya', 'Staff', 'N'),
            "{} already in the system".format(
            "Toni Kurya"))

    def test_invalid_employee_type(self):
        """
        This method tests that only staff and manager.
        """
        self.assertEqual(self.facility.add_person(
            'Toni Kurya', 'surbodinate', 'N'), "Invalid employee type.")

    def test_accomodate_staff(self):
        """
        This tests ensures that staff cannot be accomodated.
        """
        self.assertEqual(self.facility.add_person(
            'Toni Kurya', 'Staff', 'Y'),
            "Sorry only managers can be accomodated.")

    def test_reallocation_office(self):
        """
        This tests an employee reallocation to a new office
        """
        self.facility.create_room("Dojo", "office")
        self.facility.add_person('Antony Kurya', 'Staff', 'N')
        self.facility.create_room("Laravel", "office")
        self.assertEqual(self.facility.reallocate_employee(
            "Antony Kurya", "Laravel"), "{} reallocated to {}.".format(
            "Antony Kurya", "Laravel"))

    def test_reallocation_living_space(self):
        """
        This test an employee reallocation to a new living_space
        """
        self.facility.create_room("Vue", "living_space")
        self.facility.add_person('Toni Kurya', 'manager', 'Y')
        self.facility.create_room("Ember", "living_space")
        self.assertEqual(self.facility.reallocate_employee(
            "Toni Kurya", "Ember"), "{} reallocated to {}.".format(
            "Toni Kurya", "Ember"))

    def test_reallocate_employee_to_non_existing_room(self):
        """
        This tests reallocation to a room that does not exist.
        """
        self.facility.create_room("Sanic", "office")
        self.facility.add_person('Toni Kurya', 'Staff', 'N')
        self.assertEqual(self.facility.reallocate_employee(
            "Toni Kurya", "Laravel"),
            "Facility has no room with the name {}".format("Laravel"))

    def test_reallocate_to_same_office(self):
        """
        This method tests that an employee cannot be reallocated to the same room.
        """
        self.facility.create_room("Django", "office")
        self.facility.add_person('Tony Kurya', 'Staff', 'N')
        self.assertEqual(self.facility.reallocate_employee(
            "Tony Kurya", "Django"),
            "{} cannot be reallocated to the same office.".format(
                "Tony Kurya"))

    def test_reallocate_to_same_living_space(self):
        """
        This method tests that an employee cannot be reallocated to the same room.
        """
        self.facility.create_room("LAMP", "living_space")
        self.facility.add_person('Tony Kurya', 'manager', 'Y')
        self.assertEqual(self.facility.reallocate_employee(
            "Tony Kurya", "Laravel"),
            "{} cannot be reallocated to the same living space.".format(
            "Tony Kurya"))

    def test_reallocate_to_room_of_another_type(self):
        """
        This tests that an employee cannot be reallocated\
        from an office to a living space and vice versa
        """
        self.facility.create_room("Django", "office")
        self.facility.create_room("Laravel", "living_space")
        self.facility.add_person("Tony Kurya", "staff", "N")
        self.assertEqual(self.facility.reallocate_employee(
            "Tony Kurya", "Laravel"), "{} cannot be reallocated to different room type.".format("Tony Kurya"))

    def test_load_people_from_non_existing_file(self):
        """
        This method tests loading people form a file that doesn't exist.
        """
        self.facility.create_room("Knockout", "office")
        self.facility.create_room("React", "living_space")
        self.assertEqual(self.facility.load_people("employees.txt"),
                         "Error: can\'t find file or read data.")

    def test_print_allocations(self):
        """
        This method tests that allocated employees are added to a textfile.
        """
        self.facility.create_room("Montana", "office")
        self.facility.create_room("Madison", "living_space")
        self.facility.load_people("employees.txt")
        self.assertEqual(self.facility.print_allocations("allocations.txt"), "Allocations has been saved to {}".format(
            "allocations.txt"))

    def test_print_unallocated(self):
        """
        This method tests that unallocated employees are saved to a textfile.
        """
        self.facility.create_room("Rockers", "office")
        self.facility.create_room("Tacco", "living_space")
        self.facility.load_people("employee.txt")
        self.assertEqual(self.facility.print_unallocated(
            "unallocated.txt"), "Allocations has been saved to {}".format("unallocated.txt"))

    def test_print_room(self):
        """
        This tests that all employees are printed to screen.
        """
        self.facility.create_room("Mali", "office")
        self.facility.add_person("Antony Kurya", "staff", "N")
        self.assertEqual(self.facility.print_room(""),
                         "Printed all occupants on screen.")

    def test_save_state(self):
        """
        Tests the save state saves employee to database.
        """
        office = Office("boardroom", "office")
        manager = Manager("Antony Kurya", "manager", "Y")
        self.facility.offices.append(office)
        self.facility.employees.append(manager)
        self.assertEqual(self.facility.save_state("facility.db"),
                         "Employees added to database successfully.")

    def test_check_office(self):
        """
        Tests whether the object returned is office.
        """
        office = Office("techroom", "office")
        self.facility.offices.append(office)
        self.assertEqual(self.facility.check_office("techroom"), office)

    def test_check_employee(self):
        """
        Tests whether the object returned is office.
        """
        manager = Manager("Antony Kurya", "manager", "N")
        self.facility.employees.append(manager)
        self.assertEqual(self.facility.check_employee(
            "Antony Kurya"), manager)

    def test_check_living_space(self):
        """Tests whether object returned is living space"""
        space = LivingSpace("lounge", "living_space")
        self.facility.living_spaces.append(space)
        self.assertEqual(self.facility.check_living_space("lounge"), space)

    def test_check_old_employee_room(self):
        """
        Tests the previous employee room.
        """
        office = Office("HR", "office")
        self.facility.offices.append(office)
        self.facility.add_person("Antony Kurya", "manager", "N")
        self.assertEqual(self.facility.check_old_employee_room(
            "Antony Kurya"), office)

    def test_allocate_employee(self):
        """
        Tests random office returned.
        """
        office = Office("base", "office")
        self.facility.offices.append(office)
        self.assertEqual(self.facility.allocate_employee(), office)

    def test_accomodate_manager(self):
        """
        Tests random living space returned.
        """
        space = LivingSpace("sportslounge", "living_space")
        self.facility.living_spaces.append(space)
        self.assertEqual(self.facility.accomodate_manager(), space)

    def tearDown(self):
        """
        To free variables for fresh use in other tests.
        """
        self.facility.employees = []
        self.facility.offices = []
        self.facility.living_spaces = []
        self.facility.allocated_employees = []
        self.facility.unallocated_employees = []
        self.facility.allocated_rooms = []
        self.facility.unaccomodated_managers = []


if __name__ == '__main__':
    unittest.main()
