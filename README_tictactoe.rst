
OVERVIEW
========
This nodejs application uses socket.io to establish a server/client bi-directional communcation to exchange game related data.
In addition, it partially implements the perfect player game strategy of Newell and Simon's 1972 tic-tac-toe program for the machine player's game AI.

REQUIREMENTS
============
* Assumes a linux environment: e.g. ubuntu
* node.js needs to be installed.

INSTALLATION
============
All necessary nodejs modules are under ./node_modules. 
If for some reason, modules need to be downloaded, issue the following commands:
  npm install express
  npm install socket.io
  npm install nodeunit

To run the application, clone the repo and issue the following command:
  node index.js

Then point your browser to the following URL:
http://localhost:4000/
This should display an empty tic-tac-toe board.

TESTS
=====

Issue the following command to run all tests:
  ./node_modules/nodeunit/bin/nodeunit test
