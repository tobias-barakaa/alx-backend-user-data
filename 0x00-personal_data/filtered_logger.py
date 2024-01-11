#!/usr/bin/env python3
"""
    function: filter_datum
"""

def filter_datum(fields, redaction, message, separator):
    """
        function: filter_datum
    """
    for i in fields:
        message = message.replace(i + '=', i + '=' + redaction + separator)
    return message
