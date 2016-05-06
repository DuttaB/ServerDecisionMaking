"""
ECE 4574: Final Exam
File Name: systest_server_storage.py
Author: Chang Sun
Date: May 5, 2016
Description: System integration testing for server_storage.py
"""

# _________________________________________________________________________________________________


import time
import datetime
import uuid
import json
import unittest
from StringIO import StringIO
import holder
from server_storage import *


# _________________________________________________________________________________________________


class SysTestServerStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(SysTestServerStorage, self).__init__(*args, **kwargs)

    def setUp(self):
        print('******Running test case******')

    def tearDown(self):
        print('******Finished running test case******\n')

    def test1(self):
        print('Case 1: Check integration with INSERT event')


# _________________________________________________________________________________________________


if __name__ == '__main__':
    unittest.main()


# _________________________________________________________________________________________________
