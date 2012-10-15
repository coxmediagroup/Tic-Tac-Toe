all_trips_dct = {1: (1, 4, 7),
                 2: (3,),
                 3: (1, 2, 3),
                 4: (1,)
                }
all_trips = set()

def three_cons(st, inc):
    """Returns sequence of '3 in a row', starting with st and
    incremented by inc"""
    return st, st + inc, st + inc * 2

for inc, starts in all_trips_dct.iteritems():
    for start in starts:
        all_trips.add(three_cons(start, inc))
