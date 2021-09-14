import re


def company_detection_regexes():
    """
    Use this method to define a regular expression to find companies.
    The pattern list should contain only compiled regexes, to improve the performance.

    :return: List, which contains a regex, which finds companies in a string.
    """
    pattern_list = [
        re.compile(r'(?i)\b((AG)|(e\.K)|(e\.V)|(e\.G)|(i\.G)|(KG)|(GmbH))')
    ]

    return pattern_list
