"""
Usage:
     create_room  <room_name> <room_type>
     add_person <first_name> <last_name> <employee_type> [<need_accomodation>]
     reallocate_employee <first_name> <last_name> <new_room_name>
     load_people <filename>
     save_people
     load_state<dbname>
     save_state<dbname>
     print_allocated_rooms
     print_unallocated_rooms
     print_allocations [-o=<filename>]
     print_unallocated [-o=<filename>]
     print_room <room_name>
    amity (-i | --interactive)
    amity (-h | --help)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
import cmd
from docopt import docopt, DocoptExit
from clint.textui import colored

from amity import Amity


def docopt_cmd(func):
    """
    Decorator definition for the app.
    """

    def fn(self, arg):

        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            msg = "Invalid Command."

            print(msg)
            print(e)
            return

        except SystemExit:
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


amity = Amity()


class Amity(cmd.Cmd):
    print(colored.cyan('                   O8', bold=12))
    print(colored.cyan('                  @@@@C', bold=12))
    print(colored.cyan('                @@@@@@@@c', bold=12))
    print(colored.cyan('      @@@@@@@@O8@@8  8@@8o@@@@@@@@c', bold=12))
    print(colored.cyan('      @@@@@@@@            C@@@@@@@c', bold=12))
    print(colored.cyan('      8@@8                    8@@@                     O@@                                                     ', bold=12))
    print(colored.cyan('      O@@@                    @@@8                     @@@O                                                    ', bold=12))
    print(colored.cyan('      C                          C                    @@@@@8                                                   ', bold=12))
    print(colored.cyan('   o@@@@                        o@@@o                @@@ o@@8      C@@C@@@       @@@@8   @@@   @@@@                     ', bold=12))
    print(colored.cyan(' c@@@@@C                         @@@@@O             8@@c  @@@      C@@@ @@     @@ @@@C   @@@   @@@@                       ', bold=12))
    print(colored.cyan('c@@@@@c                           8@@@@o           o@@O    @@@     C@@8  @@  @@   O@@C   @@@   @@@@                      ', bold=12))
    print(colored.cyan('   @@@@@o                       8@@@@c            o@@8oooooo@@@    C@@C    @@@    o@@O   @@@   @@@@@@@@@   @@@    @@@    ', bold=12))
    print(colored.cyan('     O@o                         @@o             c@@@@@@@@@@@@@8   C@@C           o@@O   @@@   @@@@@@@@@   @@@    @@@    ', bold=12))
    print(colored.cyan('      O@@O                    O8@O               @@@         8@@o  C@@C           o@@O   @@@   @@@@        @@@    @@@    ', bold=12))
    print(colored.cyan('      8@@@                    8@@@              8@@o          O@@o C@@C           o@@O   @@@   @@@@@@@@@   @@@@@@@@@@     ', bold=12))
    print(colored.cyan('      @@@@O88O            c@8O8@@@             oOOo            OOO cOOo           cOOo   @@@   @@@@@@@@@   @@@@@@@@@@     ', bold=12))
    print(colored.cyan('      @@@@@@@@CcO@o  c@@c 8@@@@@@@c                                                                               @@@       ', bold=12))
    print(colored.cyan('      cocc     @@@@8o@@@@c    ccoc                                                                                @@@      ', bold=12))
    print(colored.cyan('                 8@@@@@C                                                                                   @@@@@@@@@@      ', bold=12))
    print(colored.cyan('                  o@@o                                                                                     @@@@@@@@@@       ', bold=12))

    print("type --help-- to view commands")
    prompt = "<--Amity-->"

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_name> <room_type>"""
        room_name = arg["<room_name>"]
        room_type = arg["<room_type>"]
        print(amity.create_room(room_name, room_type))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <employee_type> [<need_accomodation>]

        """
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        name = first_name + " " + last_name
        employee_type = arg["<employee_type>"]
        need_accomodation = arg["<need_accomodation>"]
        if need_accomodation == "":
            need_accomodation = "N"
            print(amity.add_person(name, employee_type, need_accomodation))
        else:
            print(amity.add_person(name, employee_type, need_accomodation))

    @docopt_cmd
    def do_reallocate_employee(self, arg):
        """Usage: reallocate_employee <first_name> \
        <last_name> <new_room_name>"""
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        name = first_name + " " + last_name
        new_room_name = arg["<new_room_name>"]
        print(amity.reallocate_employee(name, new_room_name))

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room [<room_name>]"""
        room_name = arg["<room_name>"]
        print(amity.print_room(room_name))

    @docopt_cmd
    def do_print_allocations(self, arg):
        """
        Usage: print_allocations [--o=<filename>]

        """
        filename = arg["--o"]
        amity.print_allocations(filename)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=<filename>]

        """
        filename = arg["--o"]
        amity.print_unallocated(filename)

    @docopt_cmd
    def do_load_state(self, arg):
        """
        Usage: load_state <dbname>

       """

        db_name = arg['<dbname>']
        amity.load_state(db_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """ Usage: load_people <filename>"""
        filename = arg["<filename>"]
        print(amity.load_people(filename))

    @docopt_cmd
    def do_save_state(self, arg):
        """
        Usage: save_state <dbname>


        """
        db_name = arg['<dbname>']
        amity.save_state(db_name)

    def do_quit(self, arg):
        """Exits the application
        """
        print("Welcome again!")
        exit()


if __name__ == '__main__':
    Amity().cmdloop()
