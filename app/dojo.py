import itertools
import random
import os

from app import person, room
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import app.models as md


MAX_OFFICE_CAP = 6
MAX_LIVING_SPACE_CAP = 4


class Dojo:
    """This class contains methods for adding persons, creating new rooms, and for returning
       all rooms or all persons in storage
    """

    def __init__(self):
        """Instantiates the Model class to allow for storage"""
        self.model = md.Model()

    @staticmethod
    def allocate_office_space(person_name, email, person_type):
        """ This methods randomly allocates an office to a fellow or staff.
            Returns True if successful and False if not
        """

        successful = True
        random.seed()

        # return the list of available offices
        all_offices = md.Model.get_list("offices")
        # return a list of offices with capacity to spare
        non_full_offices = [office
                            for office in all_offices
                            if office.current_capacity < MAX_OFFICE_CAP]
        if not non_full_offices:
            raise ValueError("There are no offices to allocate")

        if person_type == "fellow":
            random_office = random.choice(non_full_offices)
            fellow = md.Model.get_fellow(person_name, email)
            random_office.current_capacity += 1
            fellow.current_office = random_office.name
            return successful

        elif person_type == "staff":
            random_office = random.choice(non_full_offices)
            staff = md.Model.get_staff(person_name, email)
            random_office.current_capacity += 1
            staff.current_office = random_office.name
            return successful

        else:
            return not successful

    @staticmethod
    def allocate_living_space(fellow_name, email):
        """ This methods randomly allocates a living space to a fellow or staff.
            Returns True if successful and False if not
        """

        successful = True
        random.seed()

        # return a list of available living spaces
        all_living_spaces = md.Model.get_list("living_spaces")
        # return a list of living spaces with capacity to spare
        non_full_living_spaces = [living_space
                                  for living_space in all_living_spaces
                                  if living_space.current_capacity < MAX_LIVING_SPACE_CAP]

        if not non_full_living_spaces:
            raise ValueError("There are no living spaces to allocate")
        random_living_space = random.choice(non_full_living_spaces)
        fellow = md.Model.get_fellow(fellow_name, email)
        random_living_space.current_capacity += 1
        fellow.current_living_space = random_living_space.name

        return successful

    def create_new_office(self, name):
        """ Creates a new office """

        successful = True
        new_office = room.Office(name)

        # get the existing offices
        offices = md.Model.get_list("offices")
        living_spaces = md.Model.get_list("living_spaces")
        # check whether the office already exists, if it does raise an exception
        similar_office = [office for office in offices if office.name == name]
        similar_living_space = [ls for ls in living_spaces if ls.name == name]
        if similar_office or similar_living_space:
            raise ValueError("An office or living space '{}' already exists".format(name))
        self.model.update(new_office, "offices")
        return successful

    def create_new_living_space(self, name):
        """ Creates a new living space """

        successful = True
        new_living_space = room.LivingSpace(name)
        living_spaces = md.Model.get_list("living_spaces")
        offices = md.Model.get_list("offices")
        # check whether the living space already exists, if it does raise an exception
        similar_living_space = [ls for ls in living_spaces if ls.name == name]
        similar_office = [office for office in offices if office.name == name]
        if similar_living_space or similar_office:
            raise ValueError("An office or living space '{}' already exists".format(name))
        # create new living space
        self.model.update(new_living_space, "living_spaces")
        return successful

    def add_fellow(self, name, email, wants_accommodation=False):
        """ Adds a new fellow """

        new_fellow = person.Fellow(name, email)
        fellows = self.model.get_list("fellows")
        similar = [fellow for fellow in fellows if fellow.email_address == email]
        if similar:
            return "The email address provided already exists"

        self.model.update(new_fellow, "fellows")
        print("Fellow {} has been successfully added".format(new_fellow.name))
        try:
            self.allocate_office_space(new_fellow.name, email, person_type="fellow")
            print("{} has been allocated the office {}"
                  .format(new_fellow.name, new_fellow.current_office))
        except ValueError as e:
            print(e)

        if wants_accommodation:
            try:
                self.allocate_living_space(new_fellow.name, email)
                print("{} has been allocated the living space {}"
                      .format(new_fellow.name, new_fellow.current_living_space))
            except ValueError as e:
                print(e)

    def add_staff(self, name, email):
        """ Adds a new member of staff """

        new_staff = person.Staff(name, email)
        staff = self.model.get_list("staff")
        similar = [staff_member for staff_member in staff if staff_member.email_address == email]
        if similar:
            return "The email address provided already exists"

        self.model.update(new_staff, "staff")
        print("Staff {} has been successfully added".format(new_staff.name))
        try:
            self.allocate_office_space(new_staff.name, email, person_type="staff")
            print("{} has been allocated the office {}"
                  .format(new_staff.name, new_staff.current_office))
        except ValueError as e:
            print(e)

    def get_persons_by_room(self, room):
        """Returns a list of the people in the given room"""

        rooms = self.model.get_list("offices") + self.model.get_list("living_spaces")
        if room not in [room.name for room in rooms]:
            raise ValueError("The requested room does not exist")
        fellows = self.model.get_list("fellows")
        staff = self.model.get_list("staff")
        persons = staff + fellows
        persons_in_room = []
        for person in persons:
            if person.current_office == room or person.current_living_space == room:
                persons_in_room.append(person.name)
        return persons_in_room

    def print_persons_by_room(self, room_name):
        """Prints the people in the given room to screen"""

        try:
            persons_in_given_room = self.get_persons_by_room(room_name)
            is_office = self.model.get_office(room_name)
            is_living_space = self.model.get_living_space(room_name)
            if is_office:
                return "(OFFICE) {}:\n".format(room_name.upper()) + ",".join(persons_in_given_room)
            elif is_living_space:
                return "(LIVING SPACE) {}:\n".format(room_name.upper()) + ",".join(persons_in_given_room)
        except ValueError as e:
            print(e)

    def print_allocations(self, filename=None):
        """Prints all the room allocations to the screen or to a txt file"""

        staff = self.model.get_list("staff")
        fellows = self.model.get_list("fellows")

        rooms = {}

        for fellow in fellows:
            if ("L_SPACE", fellow.current_living_space) not in rooms:
                rooms[("L_SPACE", fellow.current_living_space)] = [fellow.name]
            else:
                rooms[("L_SPACE", fellow.current_living_space)] += [fellow.name]

        for person in itertools.chain(staff, fellows):
            if ("OFFICE", person.current_office) not in rooms:
                rooms[("OFFICE", person.current_office)] = [person.name]
            else:
                rooms[("OFFICE", person.current_office)] += [person.name]

        if not rooms:
            raise ValueError("No allocations have been made".upper())

        if filename:
            with open(filename + ".txt", "w") as file:
                for room, occupants in rooms.items():
                    if room[1]:
                        file_output = "{}: {}\n".format(room[0], room[1].upper()) + \
                                      "----------------------------\n" + \
                                      "{}\n\n".format(", ".join(map(str.upper, occupants)))
                        file.write(file_output)
            print("The allocations have been successfully printed to the file {}.txt".format(filename))

        else:
            output = ""

            for room, occupants in rooms.items():
                if room[1]:
                    output += "({}) {}:\n".format(room[0], room[1].upper()) + \
                              "-----------------------------\n" + \
                              "{}\n\n".format(",".join(map(str.upper, occupants)))

            return output

    def get_unallocated_persons(self):
        """Returns a dictionary with the unallocated persons"""

        staff = self.model.get_list("staff")
        fellows = self.model.get_list("fellows")
        # staff without an office
        unallocated_staff = [staff_member.name for staff_member in staff if staff_member.current_office is None]
        # fellows without an office
        unallocated_fellows_office = [fellow.name for fellow in fellows if fellow.current_office is None]
        # fellows without a living space
        unallocated_fellows_living_space = [fellow.name for fellow in fellows if fellow.current_living_space is None]

        if not unallocated_staff:
            unallocated_staff = ["No unallocated staff"]
        if not unallocated_fellows_office:
            unallocated_fellows_office = ["No unallocated fellows"]
        if not unallocated_fellows_living_space:
            unallocated_fellows_living_space = ["No unallocated fellows"]
        return {"staff": unallocated_staff,
                "fellows_office": unallocated_fellows_office,
                "fellows_living": unallocated_fellows_living_space}

    def print_unallocated(self, filename=None):
        """Prints all the unallocated persons to screen or to a txt file"""

        unallocated = self.get_unallocated_persons()

        output = "STAFF WITHOUT AN OFFICE:\n" \
                 "----------------------------\n" + \
                 "{}\n\n".format(", ".join(map(str.upper,unallocated["staff"]))) + \
                 "FELLOWS WITHOUT AN OFFICE:\n" \
                 "-----------------------------\n" + \
                 "{}\n\n".format(", ".join(map(str.upper,unallocated["fellows_office"]))) + \
                 "FELLOWS WITHOUT A LIVING SPACE:\n" \
                 "------------------------------\n" + \
                 "{}\n\n".format(", ".join(map(str.upper,unallocated["fellows_living"])))

        if filename:
            with open(filename + ".txt", "w") as file:
                file.write(output)
        else:
            return output

    def reallocate_person(self, name, email, new_room):
        """Reallocates the specified person to a new room"""

        person_to_reallocate = self.model.get_fellow(name, email) or self.model.get_staff(name, email)
        if not person_to_reallocate:
            raise ValueError("The person specified was not found")
        destination_room = self.model.get_office(new_room) or self.model.get_living_space(new_room)
        if not destination_room:
            raise ValueError("The destination room was not found")

        if isinstance(destination_room, room.Office):
            if destination_room.current_capacity >= MAX_OFFICE_CAP:
                raise OverflowError("The destination room, office {}, is full".format(destination_room))
            else:
                person_to_reallocate.current_office = destination_room.name

        elif isinstance(destination_room, room.LivingSpace):
            if destination_room.current_capacity >= MAX_LIVING_SPACE_CAP:
                raise OverflowError("The destination room, living space {}, is full".format(destination_room))
            else:
                if isinstance(person_to_reallocate, person.Staff):
                    raise ValueError("Cannot reallocate staff to a living space")
                else:
                    person_to_reallocate.current_living_space = destination_room.name

        print("{} {} has been reallocated to the {} {}".format(type(person_to_reallocate).__name__,
                                                               person_to_reallocate.name,
                                                               type(destination_room).__name__,
                                                               destination_room.name))

    def load_people_from_txt_file(self, filename):
        """Adds staff and fellows by taking the input to a txt file"""

        persons = []
        with open(filename+".txt", "r") as input_file:
            for line in input_file:
                args = line.split()
                person_email = args[0]
                wants_accommodation = False
                person_type = None

                if "Y" in args:
                    wants_accommodation = True
                    args.remove("Y")
                if "FELLOW" in args:
                    person_type = "fellow"
                    args.remove("FELLOW")
                elif "STAFF" in args:
                    person_type = "staff"
                    args.remove("STAFF")
                person_name = " ".join(args[1:])

                persons.append({"email": person_email,
                                "name": person_name.title(),
                                "type": person_type,
                                "wants_accommodation": wants_accommodation})

        fellows = [person for person in persons if person["type"] == "fellow"]
        staff = [person for person in persons if person["type"] == "staff"]

        for fellow in fellows:
            self.add_fellow(fellow["name"], fellow["email"], fellow["wants_accommodation"])
        for staff_member in staff:
            self.add_staff(staff_member["name"], staff_member["email"])

    def update_database(self, session):
        success = True
        fellows = self.model.get_list("fellows")
        for fellow in fellows:
            fellow_to_add = md.Fellow(name=fellow.name,
                                      email=fellow.email_address,
                                      current_office=fellow.current_office,
                                      current_living_space=fellow.current_living_space)
            session.add(fellow_to_add)
            session.commit()

        staff = self.model.get_list("staff")
        for staff_member in staff:
            staff_to_add = md.Staff(name=staff_member.name,
                                    email=staff_member.email_address,
                                    current_office=staff_member.current_office)
            session.add(staff_to_add)
            session.commit()

        offices = self.model.get_list("offices")
        for office in offices:
            office_to_add = md.Office(name=office.name,
                                      current_capacity=office.current_capacity)
            session.add(office_to_add)
            session.commit()

        living_spaces = self.model.get_list("living_spaces")
        for living_space in living_spaces:
            l_space = md.LivingSpace(name=living_space.name,
                                     current_capacity=living_space.current_capacity)
            session.add(l_space)
            session.commit()

        return success

    def load_from_database(self, session):
        success = True
        all_fellows = session.query(md.Fellow).all()
        print(all_fellows)
        for fellow in all_fellows:

            new_fellow = person.Fellow(fellow.name, fellow.email)
            new_fellow.current_office = fellow.current_office
            new_fellow.current_living_space = fellow.current_living_space
            self.model.update(new_fellow, "fellows")

        all_staff = session.query(md.Staff).all()
        for staff in all_staff:
            new_staff = person.Staff(staff.name, staff.email)
            new_staff.current_office = staff.current_office
            self.model.update(new_staff, "staff")

        all_offices = session.query(md.Office).all()
        for office in all_offices:
            new_office = room.Office(office.name)
            new_office.current_capacity = office.current_capacity
            self.model.update(new_office, "offices")

        all_living_spaces = session.query(md.LivingSpace).all()
        for living_space in all_living_spaces:
            new_living = room.LivingSpace(living_space.name)
            new_living.current_capacity = living_space.current_capacity
            self.model.update(new_living, "living_spaces")

        return success

    def save_state(self, database="default"):
        """Saves all the data to a database"""

        engine = create_engine("sqlite:///" + database + ".db")
        md.Base.metadata.bind = engine
        md.Base.metadata.create_all(engine)
        db_session = sessionmaker(bind=engine)
        session = db_session()

        if self.update_database(session):
            session.close()
            return "Successfully saved data to database {}".format(database)

    def load_state(self, database):
        """Loads the data stored in the database into the program"""

        if not os.path.exists(database + ".db"):
            return "The specified database does not exist"
        engine = create_engine("sqlite:///" + database + ".db")
        md.Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        session = db_session()

        if self.load_from_database(session):
            session.close()
            return "Successfully loaded data from database {}".format(database)

    @property
    def all_fellows(self):
        """Returns a list containing all the fellows added"""
        return md.Model.get_list("fellows")

    @property
    def all_staff(self):
        """Returns a list containing all added members of staff"""
        return md.Model.get_list("staff")

    @property
    def all_offices(self):
        """Return a list containing all the offices created """
        return md.Model.get_list("offices")

    @property
    def all_living_spaces(self):
        """Return a list containing all the living spaces created """
        return md.Model.get_list("living_spaces")

