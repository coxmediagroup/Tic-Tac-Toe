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




function ai_move(moves, pt) {


        moves[pt] = "player";

		var pl = new Array(0,0,0,0,0,0,0,0,0,0);
		var ai = new Array(0,0,0,0,0,0,0,0,0,0);


		var op = new Array()
		for ( x = 1; x <= moves.length; x++ ) 
               if ( moves[x-1] == "player" )
		 	        pl[x] = x; 
			else if ( !moves[x-1] )
                      ai[x] = x;		 


    pt++
//console.log((pt%3))

 	var vert = ((pt+2)%3)+1;
    if ( vert == 2 ) vert = -1
    else if ( vert == 3 ) vert = -2
//    console.log(vert)                                                                              
                                //Checks vertical row           
     moves[(ai[5] ||   ((pl[pt+3]||pl[pt-3])||(pl[pt+6]||pl[pt-6])) && (ai[pt+3]||ai[pt-3]||ai[pt+6]||ai[pt-6] )      )-1] = "ai";



    return moves


    }























