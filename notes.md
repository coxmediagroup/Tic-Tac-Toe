GameLoop
=============
- display game board
- get human input
    - should be displyed as buttons in board
- execute human move
- get ai decision
- execute ai move
- check for winner
- if winner:
    - declare and display winner
    - destroy lingering variables

Entity
-------------
- entity type (human or ai)
- get_decision() to perform actions to either
    - make a decision (if ai)
    - render page and retrieve decision (if human)
    - execute a move
- maybe subclass for human or ai to overload get_decision()?

GameBoard
=============
- collection of Rows
    - y-coordinate measured from bottom, starting at 0
- get_location(x, y) to retrieve the value of a cell

Row
-------------
- list of Locations
    - x-coordinate measured from left, starting at 0

Location
-------------
- occupying entity
- claim(entity_id) to claim location for given entity




Questions to Answer
===================
- Can I replace models.py with models/__init__.py?
- DB starts id's with 1, maybe update logic to agree


Possible Scenarios
==================

AI takes corner
---------------------
- user takes center
    - ai takes corner vertically aligned, horizontally opposed original choice
    - user takes horizontal middle vertically aligned with original and second choice
        - ai takes middle of column opposite original and second choice
        - user takes center-top
            - ai takes center-bottom
        - user takes any other cell
            - ai takes center-top
    - user takes any other cell
        - ai takes horizontal middle vertically aligned with original and second choice
- user any other cell
    - ai takes cell horizontally or vertically aligned with original choice
    - user takes cell between ai's original and second choice
        - if open, ai takes cell opposite original choice
        - otherwise, ai takes cell horizontally or vertically aligned with second choice
            - user takes center
                -ai takes cell between first and 3 choice or second and third choice
            - user any other cell
                -ai takes center
    - user takes any other cell
        - ai takes cell between ai's original and second choice

