import sys


DEBUG_PRINT = False
CONSOLE=True

def prnt(val):
    if CONSOLE:
        sys.stdout.write(val)
    

def debug_print(arg):
    
    
    if DEBUG_PRINT:
        print arg
        
        
def console_print(arg='\n'):
    if CONSOLE:
        print arg