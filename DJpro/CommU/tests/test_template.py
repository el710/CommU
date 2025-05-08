"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>

    
    Test uproject/...
"""
import unittest
import logging

class Def(unittest.TestCase):
    ## do use tests of that class
    added = True

    @classmethod
    def setUpClass(cls): 
        ## return super().setUpClass()
        logging.debug(f"Start {cls.__class__} testing ...")
    
    def setUp(self):
        ## return super().setUp()
        logging.debug("Start test ...")

    def tearDown(self):
        ## return super().tearDown()
        logging.debug("test ... over")

    @classmethod
    def tearDownClass(cls):
        ## return super().tearDownClass()
        logging.debug(f"testing {cls.__class__} is over")

    """
        Tests
    """
    @unittest.skipIf(added == False, "Test <_test> is missed")
    def test_(self):
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
    logging.basicConfig(filename=f"{__file__}_test.log", filemode="w", format="\n %(asctime)s | %(module)s | %(levelname)s | %(message)s",
                        level=logging.DEBUG, encoding="utf-8")
    
    unittest.main()