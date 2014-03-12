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
