"""Office Space Allocation app v0.0

   Usage:
       app.py create_room <room_type> <room_name>
       app.py add_person (fellow|staff) <person_name> [-y]
       app.py quit

   Options:
       -y    wants accommodation

"""

import docopt
import cmd
import person
import dojo


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

        try:
            if arg["<room_type>"] == "office":
                for room_name in arg["<room_name>"]:
                    new_office = dojo.Office().create_new(room_name)
                    if new_office:
                        print("An office called {} has been successfully created".format(room_name))
            elif arg["<room_type>"] == "living_space":
                for room_name in arg["<room_name>"]:
                    new_living_space = dojo.LivingSpace().create_new(room_name)
                    if new_living_space:
                        print("A living space called {} has been successfully created".format(room_name))
        except ValueError as e:
            print(e)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person (fellow|staff) <person_name>... [-y]

           Options:
               -y    wants accommodation
        """

        new_fellow = person.Fellow()
        new_staff = person.Staff()
        person_name = " ".join(arg["<person_name>"])

        if arg["fellow"] and arg["-y"]:
            new_fellow.add(person_name, wants_accommodation=True)

        elif arg["fellow"]:
            new_fellow.add(person_name)

        elif arg["staff"] and arg["-y"]:
            print("Staff cannot be allocated a living space")

        elif arg["staff"]:
            new_staff.add(person_name)

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        exit("You've quit the application")


if __name__ == '__main__':
    try:
        print(__doc__)
        Arguments().cmdloop()
    except KeyboardInterrupt:
        print("exiting")
