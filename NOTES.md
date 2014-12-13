
Game model
  * with standard unit tests
  * logic?


HTTP Server
  * game model per client
  * Command stream from client
  * Events published to client
  * thin controller wrapper over model
  * Persistence: Simple in-memory
  * Tests: 
    * does the tic tac toe model work as expected
    * does the command stream and events work as expected

  Node JS with Typescript?
  Python with some web app framework?
  Scala/Play/Akka?
  

Browser Client
  * Accepts input clicks from user
    * which squares can be clicked?
    * is it my turn?
  * Renders board in response to events
    * previous move of opponent, next moves shaded by winnability 
    * your next possible moves, shaded by winnability
  * Manages session with backend

  Typescript with Angular?
  Coffeescript with Angular?


CLI client?


devops concerns:

  * Develop in a vagrant image?
  * 