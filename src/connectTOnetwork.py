"""
Implements the netwrok connection i/f
Bishwajit Dutta 5/2/2016
"""

import httplib
import json

# ________________________________________________________________
      

def connectTOnetwork():
    """
    Connects to netwrok
    Parameters:
            None
    Returns:
            http connection object
            
    """
    try:
        conn = httplib.HTTPConnection('localhost:8080')
        return conn      
    except Exception as e:
        return e
    return None

# ________________________________________________________________
