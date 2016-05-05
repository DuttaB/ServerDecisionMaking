"""
ECE 4574: Final Exam
File Name: server_storage.py
Author: Chang Sun
Date: May 5, 2016
Description: Implements the various functions for storing states
             and history values of entity.
"""

# _________________________________________________________________________________________________


import datetime
import pytz
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute


# _________________________________________________________________________________________________


MAX_HISTORY_SIZE = 10


# _________________________________________________________________________________________________


class State(Model):
    """
    Storage model using pynamodb for States table.
    """
    class Meta:
        table_name = 'States'
    objectId = UnicodeAttribute(hash_key=True)
    tstamp = UTCDateTimeAttribute(range_key=True)
    state = NumberAttribute(default=0)


def create_state_table():
    """
    Creates the States table on DynamoDB.
    Preconditions:
        States table should not exist.
    Postconditions:
        States table should have been created on DynamoDB.
    Invariants:
        N/A
    """
    State.create_table(read_capacity_units=1, write_capacity_units=1)


# _________________________________________________________________________________________________


def get_all_states(objectId):
    """
    Queries the States table for all attribute values of entity with objectId.
    Returns a list of dict, where each dict is in the following format:
        {
            'tstmap': timestamp,
            'state': state
        }
    Preconditions:
        States table exists on DynamoDB.
    Postconditions:
        List of attribute values is returned properly.
    Invariants:
        Error code is given when the table doesn't exist.
    Usage examples:
        history = get_all_states(id)
    """
    items = [item.attribute_values for item in State.query(objectId)]
    items.reverse()
    return items


def get_last_states(objectId, size=1):
    """
    Returns a list of historical states/data of a particular entity
    with objectId. The list is a list of tuples (tstamp, state).
    Preconditions:
        State table exists.
    Postconditions:
        List of history states is returned properly.
    Invariants:
        - No error code should be given in this function.
        - When size is greater than history size, returns records of
          history size.
    Usage examples:
        states = get_last_states(id)  # using default size=1
        states = get_last_states(id, size=3)
    """
    history = get_all_states(objectId)
    return [(history[x]['tstamp'], history[x]['state'])
            for x in range(size if size <= len(history) else len(history))]


def store_state(objectId, state, tstamp=datetime.datetime.now()):
    """
    Stores the new state for entity with objectId.
    The default time stamp is the time when this function is invoked.
    Preconditions:
        States table exists.
    Postconditions:
        New state of the entity is stored, otherwise error code is
        provided.
    Invariants:
        - Error code is given when
            1. States table does not exist
            2. New state happens earlier than the previous state
        - Maximum entries/records for a particular entity is MAX_HISTORY_SIZE
    Usage examples:
        store_state(id, 0)      # using default time stamp
        store_state(id, 0, tstamp=datetime.datetime.now())
    """
    # localize time zone
    tstamp = pytz.utc.localize(tstamp)
    history = get_all_states(objectId)
    # error check: new state has to happen later than the previous state
    if len(history) > 0 and history[0]['tstamp'] >= tstamp:
        print("Error: New state has to happen later than previous state.")
        return
    # remove legacy history
    if len(history) > MAX_HISTORY_SIZE:
        for item in State.query(objectId):
            item.delete()
            break
    new_obj = State(objectId=objectId, tstamp=tstamp, state=state)
    new_obj.save()


# _________________________________________________________________________________________________
