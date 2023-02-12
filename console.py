#!/usr/bin/python3
"""
[HBNBCommand class]
"""
import cmd
import re
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split


class HBNBCommand(cmd.Cmd):
    """
    [HBNBCommand class]

    Args:
        cmd ([module]): [cmd module for command prompt]
    Returns:
        [bool]: [true or false]
    """
    
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,    
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, line):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """
        EOF command to exit the program
        """
        return True
    
    def emptyline(self):
        """
        [Empty line]
        """
        pass

    def default(self, line):
        """
        [default method]

        Args:
            line ([str]): [user's input]

        Returns:
            [function]: [returns the function needed or error]
        """
        lst = (line.replace('(', '.').replace(',', '.').replace(' ', '')
                [:-1].split('.'))
        if len(lst) > 1:
            if lst[1] == "all":
                return self.do_all(lst[0])

            elif lst[1] == "show":
                return self.do_show(lst[0] + ' ' + lst[2].strip('"'))

            elif lst[1] == "destory":
                return self.do_destory(lst[0] + ' ' + lst[2].strip('"'))

            elif lst[1] == "update":
                print(len(lst))
                if len(lst) == 6:
                    return self.do_update(lst[0] + ' ' + lst[2].replace('"', '') 
                            + ' ' + lst[3] + ' ' + lst[4])
                else:
                    dct = ""
                    for i in range(3, len(lst)):
                        dct += lst[i] + ","

                    dct = dct[:-1] if dct[-1]==',' else dct
                    to_dct = json.loads(dct)
                    dct_cm = {k:v for k, v in to_dct.items()}
                    for k, v in dct_cm.items():
                        key = "{}.{}".format(lst[0], lst[2].strip('\"'))
                        setattr(storage.all()[key], k, v)
                        storage.save()

            elif lst[1] == "count":
                print(len(storage.all()))

    def do_create(self, line):
        """
        Create command a new instance
        """
        line = line.split()
        if not line:
            print("** class name missing **")

        elif line[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        else:
            object = HBNBCommand.classes[line[0]]()
            object.save()
            print("{}".format(object.id))

    def do_show(self, lines):
        """
        Show command print the dict format of instance
        """
        line = lines.split()
        _all = storage.all()

        if not line:
            print("** class name missing **")

        elif line[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(lines.split()) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(lines.split()[0], lines.split()[1]) not in _all:
            print("** no instance found **")

        else:
            print(_all["{}.{}".format(lines.split()[0], lines.split()[1])])

    def do_destroy(self, lines):
        """
        Destroy command By ID
        """
        line = lines.split()
        _all = storage.all()

        if not line:
            print("** class name missing **")

        elif line[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(lines.split()) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(lines.split()[0], lines.split()[1]) not in _all:
            print("** no instance found **")

        else:
            del _all["{}.{}".format(lines.split()[0], lines.split()[1])]
            storage.save()

    def do_all(self, line):
        """
        All command Prints all string representation of \
            all instances based or not on the class name
        """
        line = line.split()
        list_all = []

        if line and line[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif not line:
            for i in storage.all().values():
                list_all.append(str(i))

        else:
            for i in storage.all().values():
                if line[0] == i.__class__.__name__:
                    list_all.append(str(i))

        if len(list_all):
            print(list_all)

    def do_update(self, lines):
        """
        Update command for resetting user attributes
        """
        line = lines.split()
        _all = storage.all()

        if not line:
            print("** class name missing **")

        elif line[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(lines.split()) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(lines.split()[0], lines.split()[1]) not in _all:
            print("** no instance found **")

        elif len(lines.split()) == 2:
            print("** attribute name missing **")

        elif len(lines.split()) == 3:
            print("** value missing **")

        else:
            key = "{}.{}".format(lines.split()[0], lines.split()[1])
            setattr(_all[key], lines.split()[2],
                re.search(r'\w+', lines.split()[3]).group())
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
