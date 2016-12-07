TypeScript Tic-Tac-Toe + Tests
=========================================
-  [Demo](http://micahbolen.github.io/Tic-Tac-Toe/)
-  [Tests](http://micahbolen.github.io/Tic-Tac-Toe/tests.html)

Protip: Watch the console for a complete play-by-play.

Tested Platforms
----------------
-  Google Chrome 33 on Mac OS X Mavericks

Thought Process
---------------
I didn't just want to write a _functional_ Tic-Tac-Toe game that never loses, so I decided that I would take
this opportunity to put a few software development best practices to work:
-  Use a _real_ design pattern.  For the purposes of this game, I chose to use the Observer Pattern.
-  Write _real_ unit tests while developing (preferrably, _before_ writing anything else).  
-  Lots of comments.
-  Lots of descriptive commits.
-  Use TypeScript.  
-  Separate logic from the UI.  

Bragging Points (sort of)
-------------------------
-  0 third-party libraries (unless you count TypeScript; which you shouldn't).
-  _Minimal_ looking at other peoples' solutions to this challenge.
-  _Minimal_ copying code from anywhere else.  Exceptions: an array intersection and an array diff function that I found elegant solutions to on StackOverflow.

If I Had More Time...
---------------------
-  Automatically generate API documentation.
-  Make the UI more whiz-bang (sound, animations, 3d).
-  Make sure everything works perfectly on all devices/browsers/OSes.