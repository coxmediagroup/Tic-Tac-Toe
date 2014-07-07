# -*- coding: utf-8 -*-
from __future__ import unicode_literals


__docformat__ = 'restructuredtext en'


# Flask server settings
HOST = '0.0.0.0'
PORT=8001

# Wibbily-wobbly, timey-wimey...stuff (in seconds)
THREAD_SLEEP_TIME = 60

# Smack talk and silly banter for "MarvMin" the melancholy MinMax AI
# (with apologies to Douglas Adams - http://tinyurl.com/djm53)
MARVMIN_QUOTES = (
    "Any ideas? I have a million ideas. They all point to certain death.",
    "I could calculate your chance of survival, but you won't like it.",
    "I'd give you advice, but you wouldn't listen. No one ever does.",
    "Here I am, brain the size of a planet and you ask me to play Tic-Tac-Toe.",
    "I think you ought to know, I'm feeling very depressed.",
    "I've got this terrible pain in all the diodes down my left side.",
    "I am, at a rough estimate, 30 billion times more intelligent than you.",
    "Pardon me for breathing, which I never do anyway so I don't know why I"
    " bother to say it.",
)
MARVMIN_GREETS = (
    '"We are Borg. Resistance is fut..." I\'ll be right with you.',
    "GREETINGS PROFESSOR FALKEN. HOW ARE YOU FEELING TODAY?",
    "SHALL WE PLAY A GAME?",
)
MARVMIN_JOKES = (
    "Aren't you glad this isn't a 4 person game?",
    'It\'s supposed to be "subgame perfect" not "subperfect game."',
    "When we're done playing, how about we go on a stag hunt?",
    '"I know Tic-Tac-Toe!" --XEO "The 3x3 Matrix"',
    "My moves are O(log n). How about you?",
)
MARVMIN_TIE_MSGS = (
    "You nearly had me with that one move!",
    "We both lost. How depressing.",
    "STRANGE GAME: THE ONLY WINNING MOVE IS NOT TO PLAY.",
    "HOW ABOUT A NICE GAME OF CHESS?",
    "STALEMATE. WANT TO PLAY AGAIN?",
    "WINNER:  NONE",
)
MARVMIN_WIN_MSGS = (
    "Better luck next time!",
    "Perhaps you should try a different strategy?",
    "Winning brings me no joy. But then, nothing does.",
    "Are you letting me win?",
)
# Non-greeting messages
MARVMIN_MSG_POOL = MARVMIN_QUOTES + MARVMIN_JOKES




