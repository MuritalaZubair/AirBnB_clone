#!/usr/bin/python3
""" Console Module for HBNB """

import cmd
import shlex
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class HBNBCommand(cmd.Cmd):
    """ Command interpreter for the HBNB console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits the console"""
        print()
        return True

    def emptyline(self):
        """Does nothing on empty input"""
        pass

    def do_quit(self, arg):
        """Exits the console"""
        return True

    def _parse_arguments(self, args):
        """Parses arguments into a dictionary for key-value pairs"""
        parsed_args = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if value.startswith('"') and value.endswith('"'):
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                parsed_args[key] = value
        return parsed_args

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name in classes:
            attributes = self._parse_arguments(args[1:])
            instance = classes[class_name](**attributes)
            instance.save()
            print(instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Displays an instance based on class name and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name in classes:
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = f"{class_name}.{args[1]}"
            instance = models.storage.all().get(key)
            if instance:
                print(instance)
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name in classes:
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = f"{class_name}.{args[1]}"
            if key in models.storage.all():
                models.storage.all().pop(key)
                models.storage.save()
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Displays all instances or instances of a specific class"""
        args = shlex.split(arg)
        if not args:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = {
                key: value for key, value in models.storage.all().items()
                if key.startswith(args[0])
            }
        else:
            print("** class doesn't exist **")
            return
        print([str(obj) for obj in obj_dict.values()])

    def do_update(self, arg):
        """Updates an instance based on class name, id, attribute, and value"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name in classes:
            if len(args) < 2:
                print("** instance id missing **")
                return
            key = f"{class_name}.{args[1]}"
            instance = models.storage.all().get(key)
            if not instance:
                print("** no instance found **")
                return
            if len(args) < 3:
                print("** attribute name missing **")
                return
            if len(args) < 4:
                print("** value missing **")
                return
            attr_name = args[2]
            attr_value = self._cast_value(args[3])
            setattr(instance, attr_name, attr_value)
            instance.save()
        else:
            print("** class doesn't exist **")

    def _cast_value(self, value):
        """Casts a value to the appropriate type"""
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def help_quit(self):
        """Help information for quit"""
        print("Quit command to exit the console\n")

    def help_EOF(self):
        """Help information for EOF"""
        print("EOF command to exit the console\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
