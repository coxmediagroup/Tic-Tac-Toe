"""
A custom exception for misplacing a token
"""

class TokenPlacementException(Exception):

    def __init__(self, value):

        self.parameter = value

    def __str__(self):

        return repr(self.parameter)
