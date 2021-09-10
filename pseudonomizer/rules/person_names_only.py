import re


def company_detection_regexes():
    pattern_list = [
        re.compile(r'(?i)\b((AG)|(e\.K)|(e\.V)|(e\.G)|(i\.G)|(KG))')
    ]

    return pattern_list
