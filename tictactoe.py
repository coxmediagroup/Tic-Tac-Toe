from random import randint
from grid import Grid
from book import Book
    
def setup_game():
    ''' Sets up the game, allowing the player to chose whether they want to 
    go first or second.
    '''
    
    while 1==1:
        choice = raw_input("Do you want to go first or second, or do you want me to decide (1/2/?): ")
        if choice[0] == '?':
            choice = str(randint(1,2))
            print "It looks like you'll be player %s!" % choice
        if choice[0] == '1':
            return 'X'
        if choice[0] == '2':
            return 'O'
        print "I'm sorry, but %s isn't valid." % choice

def start_game(grid, human):
    ''' Starts the actual tic-tac-toe game
    '''
    if human == 'O':
        ai = Book('X')        
    else:
        ai = Book('O')
        while 1==1:
            grid.print_grid()
            square = raw_input("What square would you like to fill? (1-9) ")
            if square[0] in grid.get_available():
                grid = grid.fill_square(user=human, square=square[0])
                break
            else:
                print "I'm sorry, %s isn't available." % square  
    while 1 == 1:
        grid = ai.check_grid(grid)
        if grid.test_win():
            grid.print_grid()
            print "Computer won!"
            break
        while 1==1:
            grid.print_grid()
            square = raw_input("What square would you like to fill? (1-9) ")
            available = grid.get_available()
            if square[0] not in available:
                print "I'm sorry, %s isn't available." % square
            else:
                print "Sending from game"
                grid = grid.fill_square(user=human, square=square[0])
                grid.print_grid()
                break
        if grid.test_win():
            print "You won!"
            break
        else:
            print "No one won."
                
        
        

def main():
    grid = Grid()
    print "Welcome to the unwinnable Tic-Tac-Toe\n"
    print "In this game, you will play the classic tic-tac-toe game against a computer opponent. You choose which square you want to fill by entering its number when prompted."
    human = setup_game()
    start_game(grid=grid, human=human)

if __name__=="__main__":
    main()