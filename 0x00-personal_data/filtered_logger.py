#!/usr/bin/env python3
"""
    function: filter_datum
"""

import re

def filter_datum(fields, redaction, message, separator):
    """Obfuscates specified fields in a
    log message using a regex substitution.
    """
    pattern = r"{}=(.*?)(?={})".format("|".join(fields), separator)
    return re.sub(pattern, lambda m: m.group(1).replace(m.group(2), redaction), message)

