"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>

    
    Test uproject/models/bases.py
"""
import unittest
from unittest import TestCase
import logging

# """
#     To see neighbors directory
# """
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent /"." ))

from uproject.models.bases import UtemBase
from uproject.models.uobject import UObject

class TModuleBases(TestCase):
    ## do use tests of that class
    added = True

    @classmethod
    def setUpClass(cls): 
        ## return super().setUpClass()
        logging.debug(f"Start class testing ...")
    
    def setUp(self):
        ## return super().setUp()
        logging.debug("Start test... ")

    def tearDown(self):
        ## return super().tearDown()
        logging.debug("test over")

    @classmethod
    def tearDownClass(cls):
        ## return super().tearDownClass()
        logging.debug(f"Class testing is over")

    """
        Tests
    """

    @unittest.skipIf(added == False, "Test <_test> is missed")
    def test_base(self):
        base = UtemBase()
        self.assertIsNotNone(base, "Base create error")
        item_1 = UObject("test1")
        base.add(item_1)
        self.assertIsNotNone(base.__next__(), "Add element to base error")
        self.assertIsNotNone(base.read(item_1.get_token()), "Read base error")
        item_2 = UObject("test2")
        base.add(item_2, parent_id=item_1.get_token())
        self.assertEqual(base.len(), 2, "Result of adding to base error")
        for item in base:
            self.assertIsInstance(item["utem"], UObject, "Wrong elements type")

    """
        template
    """
    @unittest.skipIf(added == False, "Test <_test> is missed")
    def _test(self):
        pass
    """
        self.assertEqual()
        self.assertAlmostEqual()
        self.assertNotEqual()
        self.assertTrue()
        self.assertIs()
        self.assertIsNone(None)
        self.assertIn()
        self.assertRaises(expected_exception=TypeError)
        self.assertWarns(expected_warning=Warning)
        self.assertLess()
        self.assertLessEqual()
    """


if __name__ == "__main__":   
    unittest.main()