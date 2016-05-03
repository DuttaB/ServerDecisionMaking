"""
ECE 4574: Final Exam
Author: Chang Sun
Date: May 5, 2016
Description: Implements the various functions for storing states
             and history values of entity.
"""

# _________________________________________________________________________________________________

from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute,
    UTCDateTimeAttribute, NumberSetAttribute, BooleanAttribute,
    JSONAttribute, UnicodeSetAttribute, BinarySetAttribute
)

# _________________________________________________________________________________________________

class State(Model):
    class Meta:
        table_name = 'States'
    buildingId = UnicodeAttribute(hash_key=True)
    state = NumberAttribute(default=0)
    tstamp = UTCDateTimeAttribute(datetime.now())

def create_state_table():
    State.create_table(read_capacity_units=1, write_capacity_units=1)

def get_states_for_building(buildingId):


# _________________________________________________________________________________________________

