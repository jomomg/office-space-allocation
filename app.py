"""Office Space Allocation app v0.0

   Usage:
       app.py create_room <room_type> <room_name>
       app.py add_person  (fellow|staff) <person_name> [-y]
       app.py do_something <something>

   Options:
       -y    wants accommodation

"""

import docopt
import cmd
import classes


def docopt_cmd(func):
    def fn(self, arg):
        try:
            opt = docopt.docopt(fn.__doc__, arg)
        except docopt.DocoptExit as e:
            print(e)
            return
        except SystemExit:
            return
        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Arguments(cmd.Cmd):
    prompt = "osa_app>>>"

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""

        if arg["<room_type>"] == "office":
            for room_name in arg["<room_name>"]:
                new_office = classes.Office().create_new(room_name)
                if new_office:
                    print("An office called {} has been successfully created".format(room_name))
        elif arg["<room_type>"] == "living_space":
            for room_name in arg["<room_name>"]:
                new_living_space = classes.LivingSpace().create_new(room_name)
                if new_living_space:
                    print("A living space called {} has been successfully created".format(room_name))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person (fellow|staff) <person_name>... [-y]

           Options:
               -y    wants accommodation
        """

        new_fellow = classes.Fellow()
        new_staff = classes.Staff()
        person_name = " ".join(arg["<person_name>"])

        if arg["fellow"] and arg["-y"]:
            new_fellow.add(person_name)
            print("Fellow {} has been successfully added".format(person_name))
            try:
                classes.Office.allocate_office_space(person_name, person_type="fellow")
                print("{} has been allocated the office {}".format(person_name, new_fellow.get_current_office(
                                                                       person_name, "fellow")))
            except ValueError as e:
                print(e)

            try:
                classes.Office.allocate_living_space(person_name)
                print("{} has been allocated the living space {}".format(person_name, new_fellow.get_current_living_space(
                                                                         person_name)))
            except ValueError as e:
                print(e)

        elif arg["fellow"]:
            new_fellow.add(person_name)
            print("Fellow {} has been successfully added".format(person_name))
            try:
                classes.Office.allocate_office_space(person_name, person_type="fellow")
                print("{} has been allocated the office {}".format(person_name, new_fellow.get_current_office(
                                                                       person_name, "fellow")))
            except ValueError as e:
                print(e)

        elif arg["staff"] and arg["-y"]:
            print("Staff cannot be allocated a living space")

        elif arg["staff"]:

            new_staff.add(person_name)
            print("Staff {} has been successfully added".format(person_name))
            try:
                classes.Office.allocate_office_space(person_name, person_type="staff")
                print("{} has been allocated the office {}".format(person_name, new_staff.get_current_office(
                                                                       person_name, "staff")))
            except ValueError as e:
                print(e)

    @docopt_cmd
    def do_something(self, arg):
        """Usage: do_something <something>"""
        print("doing {}".format(arg["<something>"]))


if __name__ == '__main__':
    try:
        print(__doc__)
        Arguments().cmdloop()
    except KeyboardInterrupt:
        print("exiting")

