"""Office Space Allocation app v0.0

   Usage:
       app.py create_room <room_type> <room_name>
       app.py add_person (fellow|staff) <person_name> [-y]
       app.py print_room <room_name>
       app.py print_allocations [-o=filename]
       app.py print_unallocated [-o=filename]
       app.py quit

   Options:
       -y             wants accommodation
       -o=filename    print information to txt file

"""

import cmd

import docopt

from app.dojo import Dojo


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

        print("")
        try:
            if arg["<room_type>"] == "office":
                for room_name in arg["<room_name>"]:
                    new_office = Dojo().create_new_office(room_name)
                    if new_office:
                        print("An office called '{}' has been successfully created".format(room_name))
            elif arg["<room_type>"] == "living_space":
                for room_name in arg["<room_name>"]:
                    new_living_space = Dojo().create_new_living_space(room_name)
                    if new_living_space:
                        print("A living space called '{}' has been successfully created".format(room_name))
        except ValueError as e:
            print(e)
        print("")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person (fellow|staff) <person_name>... [-y]

           Options:
               -y    wants accommodation
        """

        print("")
        the_dojo = Dojo()
        person_name = " ".join(arg["<person_name>"])

        if arg["fellow"] and arg["-y"]:
            the_dojo.add_fellow(person_name, wants_accommodation=True)

        elif arg["fellow"]:
            the_dojo.add_fellow(person_name)

        elif arg["staff"] and arg["-y"]:
            print("Staff cannot be allocated a living space")

        elif arg["staff"]:
            the_dojo.add_staff(person_name)
        print("")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        the_dojo = Dojo()
        room_name = arg["<room_name>"]
        print("")
        print(the_dojo.print_persons_by_room(room_name))

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [-o=filename]

           Options:
               -o=filename    print information to txt file
        """
        the_dojo = Dojo()
        print("")
        try:
            print(the_dojo.print_allocations())
            filename = arg["-o"]
            if filename:
                the_dojo.print_allocations(filename)
        except ValueError as e:
            print(e)
            print("")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [-o =filename]

           Options:
               -o=filename    print information to txt file
        """

        the_dojo = Dojo()
        print("")
        print(the_dojo.print_unallocated())
        filename = arg["-o"]
        if filename:
            the_dojo.print_unallocated(filename)

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        exit("You've quit the application")


def main():
    try:
        print(__doc__)
        Arguments().cmdloop()
    except KeyboardInterrupt:
        print("exiting")
