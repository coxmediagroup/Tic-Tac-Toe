/* Copyright 2013 Robert Edward Steckroth II <RobertSteckroth@gmail.com> Bust0ut, Surgemcgee

* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published by
* the Free Software Foundation; version 3.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Lesser General Public License for more details.
*
* You should have received a copy of the GNU Lesser General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/




function ai_move(moves, put_down) {

        moves[put_down] = "player";

		// Uhh this can be awesome here (isn't now)
		var op = new Array()
		for ( var x = 1; x <= moves.length; x++ )
              if ( ! moves[x-1] ) 
                   op.push(x)
		op.sort()




		console.log(op)
        moves[ op[0]-1] = "ai";




    return moves


    }























