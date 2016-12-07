"""ProtoRPC message definitions."""

from protorpc import messages


class GameMessage(messages.Message):
    id = messages.IntegerField(1)
    a1 = messages.StringField(2)
    a2 = messages.StringField(3)
    a3 = messages.StringField(4)
    b1 = messages.StringField(5)
    b2 = messages.StringField(6)
    b3 = messages.StringField(7)
    c1 = messages.StringField(8)
    c2 = messages.StringField(9)
    c3 = messages.StringField(10)
    outcome = messages.StringField(11)


class MoveMessage(messages.Message):
    square = messages.StringField(1)
