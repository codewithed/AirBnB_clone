#!/usr/bin/python3
"""Unittest to test file storage"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage(unittest.TestCase):
    """testing file storage functions"""

    @classmethod
    def setUp(cls):
         cls.users = User()
         cls.users.email = "307@holbertonschool.classmethod"
         cls.users.password = "12345789"
         cls.users.first_name = "Andrew"
         cls.users.last_name = "Suh"
         cls.storage = FileStorage()

    @classmethod
    def tearDown(cls):
        del cls.users
        del cls.storage

    def test_style_check(self):
        """
        Tests pep8 style
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_user_doc(self):
        """check for existance of docstrings"""
        self.assertIsNotNone(User.__doc__)
        self.assertIsNotNone(User.__init__.__doc__)
        self.assertIsNotNone(User.__str__.__doc__)
        self.assertIsNotNone(User.save.__doc__)
        self.assertIsNotNone(User.to_dict.__doc__)
    
    def test_new_object(self):
        """Tests making new instances"""
        storage_dict = self.storage.all()
        basic = BaseModel()
        self.storage.new(basic)
        key = type(basic).__name__ + "." + str(basic.id)
        self.assertIsNotNone(storage_dict[key])

        key = type(self.users).__name__ + "." + str(self.users.id)
        self.assertIsNotNone(storage_dict[key])

    def test_save_reload(self):
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        
        try:
            os.remove("file.json")
        except:
            pass

        self.storage.save()

        with open(path, 'r') as f:
            lines2 = f.readlines()

        self.assertEqual(lines, lines2)

        try:
            os.remove("file.json")
        except:
            pass

        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)