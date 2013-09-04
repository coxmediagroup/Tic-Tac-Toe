

// Yes it's a global,and it should be a global.
var nodearray= function(sel){
	return Array.prototype.slice.call(document.querySelectorAll(sel))
}

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
	moves:["four","zero","six","two","eight","seven","one","three","five"],
	
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
			
	chkforwin:function(wg){
		var results=[]
		var wl=wg.length
		while(wl--){
			if (hulk.squares.indexOf(wg[wl]) !==-1){
				results.unshift(wg[wl])
			}
		}	
		if (results.length===3){
		//If Hulk wins, remove onclick from empty squares
			var dtt=nodearray("div.tictac")
			dtt.map(tictac.rmclick)
			//highlight hulk winning squares
			var rl=results.length
			while(rl--){
				var el=document.querySelector("#"+results[rl])
				el.className +=" win"
			}
		}		
	},
			
	// Calls hulk.chkwin on each wingroup to see if Hulk won.  
	didhulkwin: function(){
		var wgl=tictac.wingroups.length 
		while(wgl--){
		var wg=tictac.wingroups[wgl]	
			hulk.chkforwin(wg)					
		}			
	}	

			
} //end hulk
		
var tictac={
		 		
	squareclass:'tictac',
		
	usedsquares:[],
	
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
		 	
	mksquares: function(){
		this.squares=nodearray('div.tictac')
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
		var squares=nodearray("div.wrap div")			
		squares.map(tictac.resetsquare)
		tictac.usedsquares=[]
		foozie.squares=[]
		hulk.squares=[]
		document.title="Tic-Tac-Toe with Hulk "
		tictac.mksquares()
	},
	
	init: function(){
		var ngd=document.querySelector("div.newgame")
		ngd.onclick=tictac.resetboard	
		tictac.resetboard()
	}		

}// end tictac 

tictac.init()
	
