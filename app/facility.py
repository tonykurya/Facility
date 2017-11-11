import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from . person import Manager, Staff
from . room import Office, LivingSpace
from . model import Base, Employees, Offices, LivingSpaces


class Facility(object):

    def __init__(self):
        self.employees = []
        self.offices = []
        self.living_spaces = []
        self.allocated_employees = []
        self.unallocated_employees = []
        self.allocated_rooms = []
        self.unaccomodated_managers = []

    def create_room(self, room_name, room_type):
        """This method creates an office or living space."""
        if room_type.lower() == "office":
            if [office
                for office in self.offices
                    if room_name == office.room_name]:
                return "{} is already created.".format(room_name)

            else:
                office = Office(room_name, room_type)
                self.offices.append(office)
                return "Office {} created successfully.".format(room_name)

        elif room_type.lower() == "living_space":
            if [living_space
                    for living_space in self.living_spaces
                    if room_name == living_space.room_name]:
                return "{} is already created.".format(room_name)
            else:
                living_space = LivingSpace(room_name, room_type)
                self.living_spaces.append(living_space)
                return "LivingSpace {} created successfully.".format(room_name)
        else:
            return "Invalid room type."

    def add_person(self, name, employee_type, need_accomodation="N"):
        """This method adds a person to the system \
        and adds them to a random room."""
        if name in [employee.name for employee in self.employees]:
            return "{} already in the system".format(name)
        else:
            if employee_type.lower() == "manager":

                if need_accomodation.upper() == "Y":
                    try:
                        manager_space = self.accomodate_manager()
                        manager = Manager(
                            name, employee_type, need_accomodation)
                        self.employees.append(manager)
                        if manager_space:
                            manager_space.room_occupants.append(name)
                            return "{}  a {} accomodated successfully".format(
                                name, employee_type)
                            self.allocated_rooms.append(manager_space)
                        else:
                            self.unaccomodated_managers.append(name)
                            print("Room is full.")
                    except:
                        self.unallocated_employees.append(name)
                        print("No living space available at the moment.")
                else:
                    try:
                        manager_office = self.allocate_employee()
                        manager = Manager(
                            name, employee_type, need_accomodation)
                        self.employees.append(manager)
                        if manager_office:
                            manager_office.room_occupants.append(name)
                            return "{}  a {} added successfully".format(
                                name, employee_type)
                        else:
                            self.unallocated_employees.append(name)
                            print("Room is full.")
                    except:
                        self.unallocated_employees.append(name)
                        print("No office space available at the moment")
            elif employee_type.lower() == "staff":
                if need_accomodation.upper() == "Y":
                    return "Sorry only managers can be accomodated."
                else:
                    try:
                        staff_room = self.allocate_employee()
                        staff = Staff(name, employee_type, need_accomodation)
                        self.employees.append(staff)
                        if staff_room:
                            staff_room.room_occupants.append(name)
                            return "{} a {} added successfully.".format(
                                name, employee_type)
                        else:
                            self.unallocated_employees.append(name)
                            print("The office is already full.")
                    except:
                        self.unallocated_employees.append(name)
                        print("No office space available at the moment")
            else:
                return "Invalid employee type."

    def allocate_employee(self):
        """This method returns a random office object."""
        if len(self.offices) == 0:
            print("No office space available.")
        else:
            secure_random = random.SystemRandom()
            random_room = secure_random.choice(self.offices)
            if len(random_room.room_occupants) < random_room.room_capacity:
                return random_room

    def accomodate_manager(self):
        """This method returns a random \
        livingspace object"""
        if self.living_spaces == 0:
            print("No living space available.")
        else:
            secure_random = random.SystemRandom()
            random_room = secure_random.choice(self.living_spaces)
            if len(random_room.room_occupants) < random_room.room_capacity:
                return random_room

    def reallocate_employee(self, employee_name, new_room_name):
        """This method reallocates an employee from one \
        livingspace or room to another."""
        if self.check_employee(employee_name):
            if self.check_office(new_room_name):
                if self.check_old_employee_room(
                        employee_name).room_name == new_room_name:
                    return "{} cannot be reallocated to the same office.".format(
                        employee_name)
                else:
                    if self.check_office(new_room_name):
                        if self.check_office(new_room_name).room_type == self.\
                                check_old_employee_room(employee_name).room_type:
                            if len(self.check_office(new_room_name).room_occupants) < 6:
                                self.check_old_employee_room(
                                    employee_name).room_occupants.remove(employee_name)
                                self.check_office(
                                    new_room_name).room_occupants.append(employee_name)
                                return "{} reallocated to {}.".format(
                                    employee_name, new_room_name)
                            else:
                                print("{} if full.".format(new_room_name))
                        else:
                            return "{} cannot be reallocated\
                            to different room type.".format(employee_name)
                    else:
                        print("{} is not an office in amity".format(new_room_name))

            elif self.check_living_space(new_room_name):
                if self.check_old_employee_room(employee_name).\
                        room_name == new_room_name:
                    return "{} cannot be reallocated to the same living space.".format(
                        employee_name)
                else:
                    if self.check_living_space(new_room_name):
                        if self.check_living_space(new_room_name).room_type == self.\
                                check_old_employee_room(employee_name).room_type:
                            if len(self.check_living_space(new_room_name).room_occupants) < 4:
                                self.check_old_employee_room(
                                    employee_name).room_occupants.\
                                    remove(employee_name)
                                self.check_living_space(
                                    new_room_name).room_occupants.append(employee_name)
                                return "{} reallocated to {}.".format(
                                    employee_name, new_room_name)
                            else:
                                print("{} if full.".format(new_room_name))
                        else:
                            return "{} cannot be reallocated to different room type.".\
                                format(employee_name)
                    else:
                        print("{} is not a living space in this facility".
                              format(new_room_name))
            else:
                return "This facility has no room with the name {}".\
                    format(new_room_name)
        else:
            print("{} is not in the system.".format(
                employee_name))

    def print_room(self, room_name):
        """This methods the people in the room name passed."""
        for rooms in self.offices + self.living_spaces:
            if rooms.room_name == room_name:
                print("---------occupants----------")
                for occupants in rooms.room_occupants:
                    print(occupants)
                return "Printed all occupants on screen."

    def print_allocations(self, filename):
        """This method prints the employees that \
        have been allocated to a textfile"""
        people = ""

        for rooms in self.living_spaces + self.offices:
            people += rooms.room_name
            people += '-' * 20 + '\n'
            if len(rooms.room_occupants) > 0:
                people += "\n".join(rooms.room_occupants)
                print(people)
            else:
                print("{} is empty.".format(rooms.room_name))

        if filename:
            with open(filename, "w") as output_file:
                output_file.write(people)
                return "Allocations has been saved to {}".format(
                    filename)
        print(people)

    def print_unallocated(self, filename):
        """This method prints the unallocated employees to a textfile."""
        employees = ""
        if self.unallocated_employees + self.unaccomodated_managers:
            employees += "\n".join(self.unallocated_employees +
                                   self.unaccomodated_managers)
            print(employees)
        else:
            print("Our waiting list is empty.")

        if filename:
            with open(filename, "w") as output_file:
                output_file.write(employees)
                return "Allocations has been saved to {}".format(
                    filename)
        print(employees)

    def check_office(self, room_name):
        """A helper method to check a room_name is an office."""
        for office in self.offices:
            if room_name == office.room_name:
                return office

    def check_living_space(self, room_name):
        """A helper method to check a room_name is a living space."""
        for space in self.living_spaces:
            if room_name == space.room_name:
                return space

    def check_employee(self, employee_name):
        """A helper method to check an employee
         from a list of all employees."""
        for employee in self.employees:
            if employee.name == employee_name:
                return employee

    def check_old_employee_room(self, employee_name):
        """A helper method to check the room an \
        employee was initially allocated."""
        for rooms in self.offices + self.living_spaces:
            if employee_name in [
                    occupants for occupants in rooms.room_occupants]:
                return rooms

    def load_state(self, db_name):
        """This method loads employees from the database to the application."""
        if db_name:
            engine = create_engine('sqlite:///{}'.format(db_name))
            print("Database created.")
        else:
            engine = create_engine('sqlite:///amity_db')
            print("Database created.")
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        try:
            get_employee = session.query(Employees).one()
            name = get_employee.employee_name
            employee_type = get_employee.employee_type
            need_accomodation = get_employee.need_accomodation
            manager = Manager(name, employee_type, need_accomodation)
            self.employees.append(manager)
            print("Employee data obtained successfully.")
        except MultipleResultsFound:
            get_employees = session.query(Employees).all()
            for employee in get_employees:
                name = employee.employee_name
                employee_type = employee.employee_type
                need_accomodation = employee.need_accomodation
                manager = Manager(name, employee_type, need_accomodation)
                self.employees.append(manager)
            print("All employee data obtained successfully.")

        except NoResultFound:
            print("The employees table is empty.")

        # gets the offices from the office table
        try:
            get_office = session.query(Offices).one()
            room_name = get_office.room_name
            room_occupants = get_office.room_occupants.split(',')
            office = Office(room_name)
            self.offices.append(office)
            get_office.room_occupants = room_occupants
            print("Office data obtained successfully.")
        except MultipleResultsFound:
            get_offices = session.query(Offices).all()
            for offices in get_offices:
                room_name = offices.room_name
                room_occupants = offices.room_occupants.split(',')
                office = Office(room_name)
                self.offices.append(office)
                office.room_occupants = room_occupants
            print("All office data obtained successfully.")

        except NoResultFound:
            print("The offices table is empty.")

        # gets livingspaces from the living_spaces table living_spaces
        try:
            get_living_spaces = session.query(LivingSpaces).one()
            room_name = get_living_spaces.room_name
            room_occupants = get_living_spaces.room_occupants.split(',')
            space = LivingSpace(room_name)
            self.living_spaces.append(space)
            print("Livingspace data obtained successfully.")
        except MultipleResultsFound:
            get_living_spaces = session.query(LivingSpaces).all()
            for spaces in get_living_spaces:
                room_name = spaces.room_name
                room_occupants = spaces.room_occupants.split(',')
                space = LivingSpace(room_name)
                self.living_spaces.append(space)
                spaces.room_occupants = room_occupants
            print("All livingspace data obtained successfully.")

        except NoResultFound:
            print("The employees table is empty.")

    def load_people(self, filename):
        """This method loads people from a \
        text file and adds them to the system."""
        try:
            employees = open(filename, "r")
            for employee in employees.readlines():
                name = employee.split()[0] + " " + employee.split()[1]
                employee_type = employee.split()[2].lower()
                if len(employee.split()) == 4:
                    need_accomodation = employee.split()[3].upper()
                else:
                    need_accomodation = "N"
                self.add_person(name, employee_type, need_accomodation)
            print("All employees loaded successfully from  textfile.")

        except IOError:
            return"Error: can\'t find file or read data."
        else:
            print("Read content from the file successfully.")

    def save_state(self, db_name):
        """This methods saves the people in the app to a database"""
        if db_name:
            engine = create_engine('sqlite:///{}'.format(db_name))
            print("Database created.")
        else:
            engine = create_engine('sqlite:///amity_db')
            print("Database created.")

        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        if self.employees:
            for employees in self.employees:
                employee = Employees(
                    employees.name, employees.employee_type,
                    employees.need_accomodation)
                try:
                    session.add(employee)
                    session.commit()
                    return "Employees added to database successfully."
                except Exception as e:
                    print("-------Error-------: {}".format(e))
                    session.rollback()
        else:
            print("Amity has no employees.")

        if self.offices:
            for rooms in self.offices:
                office_occupants = ','.join(rooms.room_occupants)
                office = Offices(
                    rooms.room_name, rooms.room_capacity, office_occupants)
                try:
                    session.add(office)
                    session.commit()
                    print("Offices added to database successfully.")
                except Exception as e:
                    print("-------Error-------: {}".format(e))
                    session.rollback()
        else:
            print("This facility has no offices.")

        if self.living_spaces:
            for spaces in self.living_spaces:
                space_occupants = ','.join(spaces.room_occupants)
                spaces = LivingSpaces(spaces.
                                      room_name, spaces.room_capacity,
                                      space_occupants)
                try:
                    session.add(spaces)
                    session.commit()
                    print("LivingSpaces added to database successfully.")
                except Exception as e:
                    print("-------Error-------: {}".format(e))
                    session.rollback()
        else:
            print("This facility has no living spaces.")

    def get_employees(self):
        """This methods returns all employee objects."""
        for employees in self.employees:
            return employees
