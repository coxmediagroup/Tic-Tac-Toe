
//Human player
var foozie={
	name:'foozie',
	squares:[]
}

//Computer		
		
var hulk={
	name:'hulk',
	squares:[],
	//order in which Hulk makes moves
	moves:["four","zero","two","six","eight","one","three","five","seven"],
			
	//if no block is needed, Hulk takes the first available move
	findmove: function(){
		var i=0
		var ml=hulk.moves.length
		while (i< ml){
			if (tictac.usedsquares.indexOf(hulk.moves[i]) !=-1){
				i++
			}else { 	
				return hulk.moves[i]
			}
		}
	},			
			
	picksquare: function(){
				
		var blk=hulk.chkwingroups()
		if (blk){
			var sq=blk
		}else{
			if (hulk.findmove()){
				var sq=hulk.findmove()
			}	
		}
		if (sq){
			tictac.setsquare(sq,hulk)
		}
		hulk.didhulkwin()			
	},		
					
	//Hulk checks wingroups to see if a block is needed
	chkwingroups: function(){
		var wgl=tictac.wingroups.length 
		while(wgl--){
			var blk= hulk.chkforblock(tictac.wingroups[wgl])
			if (blk !="noblock"){
				if(tictac.usedsquares.indexOf(blk)===-1){				
					return blk
				}
			}
					
		}
	},
			
	chkforblock: function(wingroup){
		var opensquares=[]
		var wl=wingroup.length
		while (wl--){			
			if (foozie.squares.indexOf(wingroup[wl]) ===-1){
				opensquares.unshift(wingroup[wl])
			}
		}		
		if (opensquares.length >1){
			opensquares=["noblock"]
		}
		return opensquares[0]	
	},
			
	chkwin:function(wg){
		var results=[]
		var wl=wg.length
		while(wl--){
			if (hulk.squares.indexOf(wg[wl]) !==-1){
				results.unshift(wg[wl])
			}
		}	
		if (results.length===3){
		//If Hulk wins, remove onclick from empty squares
			var dtt=Array.prototype.slice.call(document.querySelectorAll("div.tictac"))
			dtt.map(tictac.rmclick)
					 									 
		}		
	},
			
	// Calls hulk.chkwin on each wingroup to see if Hulk won.  
	didhulkwin: function(){
		var wgl=tictac.wingroups.length 
		while(wgl--){
		var wg=tictac.wingroups[wgl]	
			hulk.chkwin(wg)					
		}			
	}	

			
} //end hulk
		
var tictac={
		 		
	squareclass:'tictac',
		
	usedsquares:[],
			
	mksquares: function(){
		this.squares=Array.prototype.slice.call(document.querySelectorAll('div.tictac'))
		this.squares.map(this.addclick)
	},
			
	addclick: function(el){ 
		el.onclick=function(){ 
			tictac.setsquare(this.id,foozie)
			setTimeout(hulk.picksquare,100)
		}
		
	},		
			
	rmclick: function(el){
		el.onclick=""
	},	
	
	// there are only eight way to win the game
			//across	
	wingroups:[	["zero","one","two"], 
			["three","four","five"], 
			["six","seven","eight"],
					
			//down	
			["zero","three","six"],
			["one","four","seven"],
			["two","five","eight"], 
			
			//diagonal
			["zero","four","eight"], 
			["two","four","six"]  
	],	
		 
		 
		
	setsquare: function(square,player){
		var el=document.querySelector('#'+square)
		el.className=player.name
		tictac.usedsquares.unshift(square)
		player.squares.unshift(square)
		el.onclick=""
					
	}, 
			
	resetsquare: function(square){ 
		square.className=tictac.squareclass
	},		
			
	resetboard: function(){
		var squares=Array.prototype.slice.call(document.querySelectorAll("div.wrap div"))			
		squares.map(tictac.resetsquare)
		tictac.usedsquares=[]
		foozie.squares=[]
		hulk.squares=[]
		tictac.mksquares()
	}		

}// end tictac 


var ngd=document.querySelector("div.newgame")
ngd.onclick=tictac.resetboard	


tictac.resetboard()	