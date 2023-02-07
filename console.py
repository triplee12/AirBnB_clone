"""Command interpreter"""
import cmd


class HBNBCommand(cmd.Cmd):
    """Entery point of command interpreter"""
    
    prompt = "(hbnb)"

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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
