"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import unittest
import logging

from test_models_bases import TModuleBases

"""
    Common test Suite
"""
CommU_test = unittest.TestSuite()

"""
    Add test Cases from modules...
"""
CommU_test.addTest(unittest.TestLoader().loadTestsFromTestCase(TModuleBases))

# TModuleBases.added = False

"""
    Make & run runner
"""
logging.basicConfig(filename=f"_test.log", filemode="w", format="\n %(asctime)s | %(module)s | %(levelname)s | %(message)s",
                    level=logging.DEBUG, encoding="utf-8")

runner = unittest.TextTestRunner(verbosity=2)
runner.run(CommU_test)


