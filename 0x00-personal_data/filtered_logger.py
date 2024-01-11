#!/usr/bin/env python3
"""
    function: filter_datum
"""

import re

def filter_datum(fields, redaction, message, separator):
    """Obfuscates specified fields in a
    log message using a regex substitution.
    """
    return re.sub(
        rf'(?<=\b{"|".join(fields)}=)[^{separator}]+',
        redaction,
        message
    )
