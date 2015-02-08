Summary
=======

I did this assignment in Java because it's one of the languages I'm more familiar with than Python.
I used Spring Boot to get rid of most of the Java webapp boilerplate.  It's not very pretty, but
it's functional and covered pretty well by tests (I took a TDD approach for the most part).

Updated to use the minimax_ algorithm to guarantee the AI either wins or draws in all cases.
.. _minimax: http://en.wikipedia.org/wiki/Minimax

Requirements
============

A Java7 runtime.  This has been tested on OSX with Firefox and Chrome.

To Run
======

Clone this repository and run from the command line:

``java -jar tictactoe-0.1.0.jar``

Point your browser at http://localhost:8080/ and play away!

To Build
========

You'll need gradle.

Run ``gradle build`` at the command line.  You'll see build/libs/tictactoe-0.1.0.jar created.

To Test
=======

Run ``gradle test`` at the command line.
