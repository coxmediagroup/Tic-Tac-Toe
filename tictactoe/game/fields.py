from django.db import models
import json

class TicTacToeBoardField(models.TextField):
    """
    A model field that stores a Tic-Tac-Toe board state.
    """
    description = "A Tic-Tac-Toe board state"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(TicTacToeBoardField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value):
        return json.dumps(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value

        # Default to empty board.
        if value is None or value == '':
            return [[None, None, None],
                    [None, None, None],
                    [None, None, None]]

        return json.loads(value)
