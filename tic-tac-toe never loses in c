#include <stdio.h>
#include <conio.h>

int T[3][3];                                                 // The Tic-Tac-Toe Board
int * P = &T[0][0];                                          // Pointer to Matrix T for printBoard() function
short int i,j,userTurn=1,IWin=1000,round=0,myEvenChance=0;   // userTurn toggles turn to make move between user and me, userTurn=1 means it's user turn to play first since round=0
                                                             // IWin is set to 0 when I win no flag is uesr for human win because he can not. ;)
                                                             // Round=0 means user is to play 1st move and 1 means me first,
                                                             // At Every my 2nd chance to play 1st move is made on T[0][3] instead of T[0][0]
void showInfo(void);                                         // Shows information about the game
void initializeBoard(void);                                  // Creates 3*3 integer matrix and Initializes the board to all empty represented by 'space' ASCII >> 32
void printBoard();                                            //Prints the Board using pointer P.
                            /* Display of Board is based on ASCII
                            'space'-> 32 ~~ EMPTY
                            'O' -> 79 ~~ HUMAN
                            'X' -> 88 ~~ ME*/
int play(void);                                              // Determines who is to make move and take input from user or by myMove() and returns the move 1-9 to main function
int myMove(void);                                            // myMove return the move made by me which is 1-9
void makeMove(int);                                          // Takes the move from play and make it on board
int isOver(void);                                            // Terminate current round by returning 0
void iWin(void);                                             // iWin sets IWIN=0 so that next round can begin if i win.
void cheating(int);                                          // Terminates whole game if user try to overwrite any occupied box

void showInfo()
{
    printf("~~~~~~~~~~~~~~~~~~~~~~~~~~~~<[{(TIC-TAC~TOE)}]>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\a");
    printf("You Are 'O' & I'm 'X'\n");
    printf("Objective : Try To Get 3 Consecutive 'O's (naughts) To Win.\n");
    printf("You Are To Play First And Then The Side Changes Every Round.\n");
    printf("%c %c %c %c %c %c %c %c %c %c %c >>>>> PS: YOU CAN NEVER WIN!! <<<<< %c %c %c %c %c %c %c %c %c %c %c\n",2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1);
}
void initializeBoard()
{
    for(i=0;i<3;i++)
      for(j=0;j<3;j++)
        T[i][j]=32;
}
void printBoard()
{
  P = &T[0][0];
  printf("\n");
  for(i=1;i<=5;i++)
  { printf(" ");
    if(i%2!=0)
    {
     for(j=1;j<=5;j++)
     {
       if(j%2==0)
       printf("|");
       else{
       printf("%3c",*P);
       P++;
       }
     }
    }else
    printf("\n -----------\n");
  }
}
int play()
{
    int move=0;
    if(userTurn)
    {
        printf("\n Your Turn! Input a move.\n");
ASKAGAIN:
        scanf("%d",&move);
        if(move>9||move<1)
        {
          printf("\n%d is not a valid move! Enter 1-9\n",move);
        goto ASKAGAIN;
        }
        userTurn=0;
    }else {
     move= myMove();
     userTurn=1;
    }
    return move;
}
int myMove()
{
    int move=0;
   do{
    if(T[0][0]==88&&T[0][1]==88&&T[0][2]==32)
        {move=3;iWin();break;}
    if(T[0][0]==88&&T[0][2]==88&&T[0][1]==32)
        {move=2;iWin();break;}
    if(T[0][1]==88&&T[0][2]==88&&T[0][0]==32)
        {move=1;iWin();break;}
    if(T[1][0]==88&&T[1][1]==88&&T[1][2]==32)
        {move=6;iWin();break;}
    if(T[1][0]==88&&T[1][2]==88&&T[1][1]==32)
        {move=5;iWin();break;}
    if(T[1][1]==88&&T[1][2]==88&&T[1][0]==32)
        {move=4;iWin();break;}
    if(T[2][0]==88&&T[2][1]==88&&T[2][2]==32)
        {move=9;iWin();break;}
    if(T[2][0]==88&&T[2][2]==88&&T[2][1]==32)
        {move=8;iWin();break;}
    if(T[2][1]==88&&T[2][2]==88&&T[2][0]==32)
        {move=7;iWin();break;}
    if(T[0][0]==88&&T[1][0]==88&&T[2][0]==32)
        {move=7;iWin();break;}
    if(T[0][0]==88&&T[2][0]==88&&T[1][0]==32)
        {move=4;iWin();break;}
    if(T[1][0]==88&&T[2][0]==88&&T[0][0]==32)
        {move=1;iWin();break;}
    if(T[0][1]==88&&T[1][1]==88&&T[2][1]==32)
        {move=8;iWin();break;}
    if(T[0][1]==88&&T[2][1]==88&&T[1][1]==32)
        {move=5;iWin();break;}
    if(T[1][1]==88&&T[2][1]==88&&T[0][1]==32)
        {move=2;iWin();break;}
    if(T[0][2]==88&&T[1][2]==88&&T[2][2]==32)
        {move=9;iWin();break;}
    if(T[0][2]==88&&T[2][2]==88&&T[1][2]==32)
        {move=6;iWin();break;}
    if(T[1][2]==88&&T[2][2]==88&&T[0][2]==32)
        {move=3;iWin();break;}
    if(T[0][0]==88&&T[1][1]==88&&T[2][2]==32)
        {move=9;iWin();break;}
    if(T[0][0]==88&&T[2][2]==88&&T[1][1]==32)
        {move=5;iWin();break;}
    if(T[1][1]==88&&T[2][2]==88&&T[0][0]==32)
        {move=1;iWin();break;}
    if(T[0][2]==88&&T[1][1]==88&&T[2][0]==32)
        {move=7;iWin();break;}
    if(T[0][2]==88&&T[2][0]==88&&T[1][1]==32)
        {move=5;iWin();break;}
    if(T[1][1]==88&&T[2][0]==88&&T[0][2]==32)
        {move=3;iWin();break;}
    if(T[0][0]==79&&T[0][1]==79&&T[0][2]==32)
        {move=3;break;}
    if(T[0][0]==79&&T[0][2]==79&&T[0][1]==32)
        {move=2;break;}
    if(T[0][1]==79&&T[0][2]==79&&T[0][0]==32)
        {move=1;break;}
    if(T[1][0]==79&&T[1][1]==79&&T[1][2]==32)
        {move=6;break;}
    if(T[1][0]==79&&T[1][2]==79&&T[1][1]==32)
        {move=5;break;}
    if(T[1][1]==79&&T[1][2]==79&&T[1][0]==32)
        {move=4;break;}
    if(T[2][0]==79&&T[2][1]==79&&T[2][2]==32)
        {move=9;break;}
    if(T[2][0]==79&&T[2][2]==79&&T[2][1]==32)
        {move=8;break;}
    if(T[2][1]==79&&T[2][2]==79&&T[2][0]==32)
        {move=7;break;}
    if(T[0][0]==79&&T[1][0]==79&&T[2][0]==32)
        {move=7;break;}
    if(T[0][0]==79&&T[2][0]==79&&T[1][0]==32)
        {move=4;break;}
    if(T[1][0]==79&&T[2][0]==79&&T[0][0]==32)
        {move=1;break;}
    if(T[0][1]==79&&T[1][1]==79&&T[2][1]==32)
        {move=8;break;}
    if(T[0][1]==79&&T[2][1]==79&&T[1][1]==32)
        {move=5;break;}
    if(T[1][1]==79&&T[2][1]==79&&T[0][1]==32)
        {move=2;break;}
    if(T[0][2]==79&&T[1][2]==79&&T[2][2]==32)
        {move=9;break;}
    if(T[0][2]==79&&T[2][2]==79&&T[1][2]==32)
        {move=6;break;}
    if(T[1][2]==79&&T[2][2]==79&&T[0][2]==32)
        {move=3;break;}
    if(T[0][0]==79&&T[1][1]==79&&T[2][2]==32)
        {move=9;break;}
    if(T[0][0]==79&&T[2][2]==79&&T[1][1]==32)
        {move=5;break;}
    if(T[1][1]==79&&T[2][2]==79&&T[0][0]==32)
        {move=1;break;}
    if(T[0][2]==79&&T[1][1]==79&&T[2][0]==32)
        {move=7;break;}
    if(T[0][2]==79&&T[2][0]==79&&T[1][1]==32)
        {move=5;break;}
    if(T[1][1]==79&&T[2][0]==79&&T[0][2]==32)
        {move=3;break;}
  }while(1>10);
  if(move==0&&round==1&&myEvenChance==1)
    move= T[0][2]==32?3:T[2][0]==32?7:T[1][1]==32?5:T[1][2]==32?6:T[2][1]==32?8:9;
  else if(move==0)
    move= T[1][1]==32?5:T[2][2]==32?9:T[0][0]==32?1:T[0][2]==32?3:T[0][1]==32?2:T[2][0]==32?7:T[1][2]==32?6:T[1][0]==32?4:8;
  return move;
}

void makeMove(int move)
{  if(!userTurn)
  {
    switch (move)
    {
    case 1:
        if(T[0][0]!=32){
          cheating(move);
        }
        T[0][0]=79;break;
    case 2:
        if(T[0][1]!=32){
          cheating(move);
        }
        T[0][1]=79;break;
    case 3:
        if(T[0][2]!=32){
          cheating(move);
        }
        T[0][2]=79;break;
    case 4:
        if(T[1][0]!=32){
          cheating(move);
        }
        T[1][0]=79;break;
    case 5:
        if(T[1][1]!=32){
          cheating(move);
        }
        T[1][1]=79;break;
    case 6:
        if(T[1][2]!=32){
          cheating(move);
        }
        T[1][2]=79;break;
    case 7:
        if(T[2][0]!=32){
          cheating(move);
        }
        T[2][0]=79;break;
    case 8:
        if(T[2][1]!=32){
          cheating(move);
        }
        T[2][1]=79;break;
    case 9:
        if(T[2][2]!=32){
          cheating(move);
        }
        T[2][2]=79;break;
    }
  }else{
        switch (move)
    {
    case 1:
        T[0][0]=88;break;
    case 2:
        T[0][1]=88;break;
    case 3:
        T[0][2]=88;break;
    case 4:
        T[1][0]=88;break;
    case 5:
        T[1][1]=88;break;
    case 6:
        T[1][2]=88;break;
    case 7:
        T[2][0]=88;break;
    case 8:
        T[2][1]=88;break;
    case 9:
        T[2][2]=88;break;
  }
 }
}

int isOver()
{
    int gameNotOver=1000;
    for(i=0;i<3;i++)
    {
     for(j=0;j<3;j++)
      {
      gameNotOver =T[i][j];
      if(gameNotOver==32)
        return gameNotOver;
      }
    }
      return 0;
}
iWin()
{
    printf("\n I WIN! YOU LOSE! %c\n",2);
    IWin=0;
}
void cheating(int n)
{
    printf("\nThe Position %d is already occupied!\n",n);
    printf("\nYou can not make a move there........ CHEATER...............!!!!! \n");
    printf("press a key followed by enter");
    scanf("%d",&i);
    while(1)
    {
        printf("Game Over                                                                        \n");
        printf("         Game Over                                                               \n");
        printf("                  Game Over                                                      \n");
        printf("                           Game Over                                             \n");
        printf("                                    Game Over                                    \n");
        printf("                                             Game Over                           \n");
        printf("                                                      Game Over                  \n");
        printf("                                                               Game Over         \n");
        printf("                                                                        Game Over\n");
        printf("                                                               Game Over         \n");
        printf("                                                      Game Over                  \n");
        printf("                                             Game Over                           \n");
        printf("                                    Game Over                                    \n");
        printf("                           Game Over                                             \n");
        printf("                  Game Over                                                      \n");
        printf("         Game Over                                                               \n");
        printf("Game Over                                                                        \n");
    }

}


void main()
{
    int gameNotOver=1,over=1,input=1000,roundCount=0;           /*gameNot Over=1 means game is not over over
                                                                input is used to exit on round completion
                                roundCount count round to change my 1st move on every 2nd time of my 1st to move occurance*/
    showInfo();
NEXTROUND :
    roundCount++;
    myEvenChance=roundCount%4==0?1:0;
    initializeBoard();
  while(gameNotOver!=0)
  {
    userTurn?printBoard():printf("\n");                               // To Not print the board before i makes move
    int move = play();
    makeMove(move);
    if(IWin==0){
        printBoard();
        break;}
    gameNotOver= isOver();
  }
   if(IWin!=0)
      printBoard();
   printf("\n\n Game Over!\n\a");
   round=round==0?1:0,userTurn=round==1?0:1,IWin=1000,gameNotOver=1000;
   printf("\nInput 0 for next round OR any key to exit >>\n\n");
   scanf("%d",&input);
   if(input==0)
   {
      goto NEXTROUND;
   }else
    getch();
}
