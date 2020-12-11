import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')


def to_snake_case(string):
    return pattern.sub('_', string).lower()
