"""
ECE 4574: Final Exam
File Name: unittest_server_storage.py
Author: Chang Sun
Date: May 5, 2016
Description: Unit testing for server_storage.py
"""

# _________________________________________________________________________________________________


import datetime
import uuid
import unittest
from StringIO import StringIO
from server_storage import *


# _________________________________________________________________________________________________


class UnitTestServerStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(UnitTestServerStorage, self).__init__(*args, **kwargs)

    def test(self):
        print('******Running test cases******')

        id1 = str(uuid.uuid4())
        id2 = str(uuid.uuid4())
        id3 = str(uuid.uuid4())

        times = [datetime.datetime.now()]
        for i in range(2 * MAX_HISTORY_SIZE - 1):
            times.append(times[i] + datetime.timedelta(seconds=30))

        # Case 1
        print('Case 1: Check empty list if object does not exist')
        history = get_all_states(id1)
        self.assertEqual(history, [])

        # Case 2
        print('Case 2: Check normal operation')
        size1 = 6
        for i in range(size1):
            store_state(id1, i, times[i])
        history1 = get_last_states(id1, size=size1)
        self.assertEqual(size1, len(history1))
        for i in range(1, len(history1)):
            self.assertEqual(True, history1[i-1][0] > history1[i][0])

        # Case 3
        print('Case 3: Check size > MAX_HISTORY_COUNT')
        size2 = MAX_HISTORY_SIZE + 1
        for i in range(size2):
            store_state(id2, i, times[i])
        history2 = get_last_states(id2, size=size2)
        self.assertEqual(MAX_HISTORY_SIZE, len(history2))
        for i in range(1, len(history2)):
            self.assertEqual(True, history2[i-1][0] > history2[i][0])

        # Case 4
        print('Case 4: Check current state time stamp later than previous state')
        earlier = times[0]
        later = times[1]
        out = StringIO()
        store_state(id3, 0, tstamp=earlier, out=out)
        store_state(id3, 0, tstamp=later, out=out)
        output = out.getvalue().strip()
        self.assertEqual(output, '')

        # Case 5
        print('Case 5: Check current state time stamp earlier than previous state')
        earlier = times[2]
        later = times[3]
        store_state(id3, 0, tstamp=later, out=out)
        store_state(id3, 0, tstamp=earlier, out=out)
        output = out.getvalue().strip()
        self.assertEqual(output, 'Error: New state has to happen later than previous state.')

        print('******Finished running test cases******')


# _________________________________________________________________________________________________


if __name__ == '__main__':
    unittest.main()


# _________________________________________________________________________________________________
