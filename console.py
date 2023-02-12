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
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()
    
    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

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

    def do_update(self, args):
        """
        Update command for resetting user attributes
        """
        _all = storage.all()
        if len(args.split()) == 0:
            print("** class name missing **")

        elif args.split()[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")

        elif len(args.split()) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(args.split()[0], args.split()[1]) not in _all:
            print("** no instance found **")

        elif len(args.split()) == 2:
            print("** attribute name missing **")

        elif len(args.split()) == 3:
            print("** value missing **")
        else:
            key = "{}.{}".format(args.split()[0], args.split()[1])
            setattr(_all[key], args.split()[2],
                    re.search(r'\w+', args.split()[3]).group())
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
