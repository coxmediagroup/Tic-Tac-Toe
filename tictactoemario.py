#-------------------------------------------------------------------------------
# Name:        Tic Tac Toe - By Demario
# Purpose:     Fun interactive tic tac toe game
#-------------------------------------------------------------------------------
from random import choice as rc
posnval={1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9}

def bad_input():
    print 'bad input'

def board_values():
    print ' '
    print '%s | %s | %s' % (posnval[7],posnval[8],posnval[9])
    print '- + - + -'
    print '%s | %s | %s' % (posnval[4],posnval[5],posnval[6])
    print '- + - + -'
    print '%s | %s | %s' % (posnval[1],posnval[2],posnval[3])
    print ' '
    
def board_reset():
    for i in range(10):
        if i==0:
            pass
        else:
            posnval[i]=i

def display_help():
    print '\nPress the number for location'
    print '\nComputer is always first till you win'
    raw_input('\nHit enter to continue: ')

def game_menu():
    while True:
        print '1 - Display Help'
        print '2 - Start Game'
        print '3 - Exit'
        gc=raw_input('1, 2, 3: ')
        if gc==1 or gc=='1':
            display_help()
        elif gc==2 or gc=='2':
            board_reset()
            player_vs_computer()
        elif gc==3 or gc=='3':
            break

def npc_turn(npc):
    empty_spaces=[]
    
    x=[]
    o=[]
    corner=[1,3,7,9]
    sides=[2,4,6,8]
    center=[5]
    for i in posnval:
        if i==posnval[i]:
            empty_spaces.append(i)
        elif posnval[i]=='X':
            x.append(i)
        elif posnval[i]=='O':
            o.append(i)
    #print empty_spaces
    #print x
    #print o
    
    if len(empty_spaces)==9:
        posnval[rc([5])]=npc

    if len(empty_spaces)==7:
        if 5 in x: #checks if first move center
            #print 'We have center first'
            for i in corner: #if opponent in corner
                if i in o: 
                    if 1 in o:
                        posnval[9]=npc
                    if 3 in o:
                        posnval[7]=npc
                    if 7 in o:
                        posnval[3]=npc
                    if 9 in o:
                        posnval[1]=npc
            for i in sides:
                if i in o:
                    if i ==2:
                        posnval[rc([7,9])]=npc
                    if i ==4:
                        posnval[rc([3,9])]=npc
                    if i ==6:
                        posnval[rc([1,7])]=npc
                    if i ==8:
                        posnval[rc([1,3])]=npc        
        else:   #if 1st move!=center:1st move=corner
            for i in corner:
                if i in x:
                    print 'We have corner corner first'

    if len(empty_spaces)==5:
        moved=False
        if 5 in x:
            for corners in corner:
                if corners in x:
                    if corners<5:
                        spot=5-corners+5
                    else:
                        spot=5-(corners-5)
                    if spot in empty_spaces and moved==False:
                        posnval[spot]=npc
                        moved=True
                                 

        for pcmove in sides:
            if pcmove in o:
                if pcmove+1 in o:
                    if pcmove-1 in empty_spaces and moved!=True:
                        posnval[pcmove-1]=npc
                        moved=True
                if pcmove-1 in o:
                    if pcmove+1 in empty_spaces and moved!=True:
                        posnval[pcmove+1]=npc
                        moved=True
                if pcmove-3 in o:
                    if pcmove+3 in empty_spaces and moved!=True:
                        posnval[pcmove+3]=npc
                        moved=True
                if pcmove+3 in o:
                    if pcmove-3 in empty_spaces and moved!=True:
                        posnval[pcmove-3]=npc
                        moved=True
        for pcmove in corner:
            if 1 in o and 7 in o and 4 in empty_spaces and moved!=True:
                posnval[4]=npc
                moved=True
            if 1 in o and 3 in o and 2 in empty_spaces and moved!=True:
                posnval[2]=npc
                moved=True
            if 7 in o and 9 in o and 8 in empty_spaces and moved!=True:
                posnval[8]=npc
                moved=True
            if 9 in o and 3 in o and 6 in empty_spaces and moved!=True:
                posnval[6]=npc
                moved=True

        for c in corner:
            if c in x:
                if c==1:
                    pass
                if c==3:
                    pass
                if c==7:
                    pass
                if c ==9:
                    pass
        if moved==False:
            #print'Missing Protocol 5.'
            posnval[rc(empty_spaces)]=npc

    if len(empty_spaces)==3:
        moved=False
        for npcmove in corner:
            if 1 in x and 7 in x and 4 in empty_spaces and moved!=True:
                posnval[4]=npc
                moved=True
            if 1 in x and 3 in x and 2 in empty_spaces and moved!=True:
                posnval[2]=npc
                moved=True
            if 7 in x and 9 in x and 8 in empty_spaces and moved!=True:
                posnval[8]=npc
                moved=True
            if 9 in x and 3 in x and 6 in empty_spaces and moved!=True:
                posnval[6]=npc
                moved=True
        if 5 in x:
            for corners in corner:
                if corners in x:
                    if corners<5:
                        spot=5-corners+5
                    else:
                        spot=5-(corners-5)
                    if spot in empty_spaces and moved==False:
                        posnval[spot]=npc
                        moved=True
        for pw in x:
            u1=pw+3
            u2=pw+6
            d1=pw-3
            d2=pw-6
            if u1 in x and u2 in empty_spaces and moved!=True:
                posnval[u2]=npc
                moved=True
            if d1 in x and d2 in empty_spaces and moved!=True:
                posnval[d2]=npc
                moved=True               
        if moved==False:
            #print'Missing Protocol 3.'
            posnval[rc(empty_spaces)]=npc
            
    if len(empty_spaces)<=2:
        moved=False
        if 5 in x:
            for corners in corner:
                if corners in x:
                    if corners<5:
                        spot=5-corners+5
                    else:
                        spot=5-(corners-5)
                    if spot in empty_spaces and moved==False:
                        posnval[spot]=npc
                        moved=True
                                 

        for pcmove in sides:
            if pcmove in o:
                if pcmove+1 in o:
                    if pcmove-1 in empty_spaces and moved!=True:
                        posnval[pcmove-1]=npc
                        moved=True
                if pcmove-1 in o:
                    if pcmove+1 in empty_spaces and moved!=True:
                        posnval[pcmove+1]=npc
                        moved=True
                if pcmove-3 in o:
                    if pcmove+3 in empty_spaces and moved!=True:
                        posnval[pcmove+3]=npc
                        moved=True
                if pcmove+3 in o:
                    if pcmove-3 in empty_spaces and moved!=True:
                        posnval[pcmove-3]=npc
                        moved=True
        for pcmove in corner:
            if 1 in o and 7 in o and 4 in empty_spaces and moved!=True:
                posnval[4]=npc
                moved=True
            if 1 in o and 3 in o and 2 in empty_spaces and moved!=True:
                posnval[2]=npc
                moved=True
            if 7 in o and 9 in o and 8 in empty_spaces and moved!=True:
                posnval[8]=npc
                moved=True
            if 9 in o and 3 in o and 6 in empty_spaces and moved!=True:
                posnval[6]=npc
                moved=True

        #for c in corner:
            #if c in x:
                #if c==1:
                    #print 'c is 1'
               # if c==3:
              #      print 'c is 3'
              #  if c==7:
               #     print 'c is 7'
               # if c ==9:
               #     print 'c is 9'
        for pw in x:
            u1=pw+3
            u2=pw+6
            d1=pw-3
            d2=pw-6
            if u1 in x and u2 in empty_spaces and moved!=True:
                posnval[u2]=npc
                moved=True
            if d1 in x and d2 in empty_spaces and moved!=True:
                posnval[d2]=npc
                moved=True
        if moved!= True:
            posnval[rc(empty_spaces)]=npc            
        

def pc_turn(pc):
    board_values()
    value_location(pc)



def player_vs_computer():
    print '\nWelcome challenger'
    print '\nDefeat me to earn first move'
    raw_input('\nHit enter to start')
    status_checker()


def status_checker(pc='O',npc='X',turn='npcturn'):
    while True:
        
        if posnval[1]==posnval[2]==posnval[3]:
            board_values()
            print 'Player',posnval[1],'wins.'
            break
        if posnval[4]==posnval[5]==posnval[6]:
            board_values()
            print 'Player',posnval[4],'wins.'
            break
        if posnval[7]==posnval[8]==posnval[9]:
            board_values()
            print 'Playerl',posnval[7],'wins.'
            break
        if posnval[1]==posnval[4]==posnval[7]:
            board_values()
            print 'Player',posnval[1],'wins.'
            break
        if posnval[2]==posnval[5]==posnval[8]:
            board_values()
            print 'Player',posnval[2],'wins.'
            break
        if posnval[3]==posnval[6]==posnval[9]:
            board_values()
            print 'Player',posnval[3],'wins.'
            break
        if posnval[3]==posnval[5]==posnval[7]:
            board_values()
            print 'Player',posnval[3],'wins.'
            break
        if posnval[1]==posnval[5]==posnval[9]:
            board_values()
            print 'Player',posnval[1],'wins.'
            break
                posmoves=[]        
        for i in posnval:
                if i==posnval[i]:
                    posmoves.append(i)
        if len(posmoves)==0:
            print '\nYou have not beaten me\n'
            break

        if turn=='npcturn':
            npc_turn(npc)
            turn='pcturn'
        else:
            pc_turn(pc)
            turn='npcturn'

        

def value_location(usercode):
    vl=True
    while vl==True:
        try:
            uvi=int(raw_input('Your Move '))
            if uvi in posnval:
                if posnval[uvi]==uvi:
                    posnval[uvi]=usercode
                    vl=False
                else:
                    bad_input()
                    board_values()
            else:
                bad_input()
                board_values()
        except:
            bad_input()
            board_values()

def main():
    game_menu()

main()
