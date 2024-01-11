#!/usr/bin/env python3
"""
    function: filter_datum
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
        function: filter_datum
    """
    return re.sub(r'(?<=\b' + '|'.join(fields) + r')=([^{}]+)'.format(separator), '=' + redaction, message)

