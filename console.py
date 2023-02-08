"""
Command interpreter
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """
    Entery point of command interpreter
    Args:
        cmd ([module]): [cmd module for command prompt]
    Returns:
        [bool]: [true or false]
    """
    
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel
    }

    def do_quit(self, line):
        """
        Quits the command interpreter
        """
        return True

    def do_EOF(self, line):
        """Exit the command interpreter"""
        return True
    
    def emptyline(self):
        """
        Empty line
        """
        pass

    def do_create(self, line):
        """Creates a new instance of class."""
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
        Prints the string representation of an instance 
        based on the class name and id.
        """
        line = lines.split()
        _all = storage.all()

        if not line:
            print("** class name missing **")
        elif line[0] not in HBNBCommand.classes.keys():
            print("** class name doesn't exist **")
        elif len(lines.split()) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(lines.split()[0], lines.split()[1]) not in _all:
            print("** no instance found **")
        else:
            print(_all["{}.{}".format(lines.split()[0], lines.split()[1])])
    
    def do_destory(self, lines):
        """
        Deletes the instance from the database 
        using the given class and id.
        """
        line = lines.split()
        _all = storage.all()

        if not line:
            print("** class name missing **")
        elif line[0] not in HBNBCommand.classes.keys():
            print("** class name doesn't exist **")
        elif len(lines.split()) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(lines.split()[0], lines.split()[1]) not in _all:
            print("** no instance found **")
        else:
            del _all["{}.{}".format(lines.split()[0], lines.split()[1])]
            storage.save()
    
    def do_all(self, line):
        """Prints all string representation of all 
        instances based or not on the class name.
        """
        line = line.split()
        list_all = []

        if line and line[0] not in HBNBCommand.classes.keys():
            print("** class name doesn't exist **")
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
        """Updates an instance based on the class name and 
        id by adding or updating attribute.
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