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
        rf'({"|".join(f"(?:{re.escape(field)})" for field in fields)})=[^{separator}]+',
        rf'\1={redaction}',
        message
    )
