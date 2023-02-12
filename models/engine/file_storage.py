#!/usr/bin/python3
"""Module for FileStorage class."""
import datetime
import json
from os import path
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    classes = {"BaseModel": BaseModel,
               "User": User,
               "State": State,
               "City": City, "Amenity": Amenity,
               "Place": Place,
               "Review": Review}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        FileStorage.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(objdict, f)

    def reload(self):
        """[reload]
        """
        if path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as f:
                obj = json.load(f)
                dct = {}
                for k, v in obj.items():
                    dct[k] = self.classes[v["__class__"]](**v)
                FileStorage.__objects = dct
        else:
            return
