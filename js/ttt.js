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
	moves:["four","six","two","eight","zero","seven","one","three","five","four"],
			
	//if no block is needed, Hulk takes the first available move
	findmove: function(){
		var i=0
		var ml=hulk.moves.length
		var used=tictac.usedsquares.join()
		while (i< ml){
			if (used.match(hulk.moves[i])){
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
				var used=tictac.usedsquares.join()
				if (used.match(blk)){
				;			
				} else {
					return blk
				}
			}
					
		}
	},
			
	chkforblock: function(wingroup){
		var opensquares=[]
		var wl=wingroup.length
		var fs=foozie.squares.join()
		while (wl--){			
			if (fs.match(wingroup[wl])) {
					;
			}else{		
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
		var hs=hulk.squares.join()
		while(wl--){
			if (hs.match(wg[wl])){
				results.unshift(wg[wl])
			}else{
			}	
			if (results.length===3){
				var wrap=document.getElementById("wrap")
				var squares=Array.prototype.slice.call(wrap.children)	
				
				var sl=squares.length
				while(sl--){
					tictac.rmclick(squares[sl])
				}	
				//highlight hulk winning squares
				var rl=results.length
				while(rl--){
					var el=document.getElementById(results[rl])
					el.className +=" win"
				}
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
		var wrap=document.getElementById("wrap")
		this.squares=Array.prototype.slice.call(wrap.children)	
		var sl=this.squares.length
				while(sl--){
					tictac.addclick(this.squares[sl])
				}	
		
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
		var el=document.getElementById(square)
		el.className=player.name
		tictac.usedsquares.unshift(square)
		player.squares.unshift(square)
		el.onclick=""
					
	}, 
			
	resetsquare: function(square){ 
		square.className=tictac.squareclass
	},		
			
	resetboard: function(){
		var wrap=document.getElementById("wrap")
		var squares=Array.prototype.slice.call(wrap.children)
		var sl=squares.length
		while (sl--){		
			tictac.resetsquare(squares[sl])
		}
		tictac.usedsquares=[]
		foozie.squares=[]
		hulk.squares=[]
		document.title="Tic-Tac-Toe with Hulk "
		tictac.mksquares()
 		tictac.setsquare("four",hulk)
	},
	
	init: function(){
		var ngd=document.getElementById("newgame")
		ngd.onclick=tictac.resetboard	
		tictac.resetboard()
 tictac.setsquare("four",hulk)
	}
}// end tictac 

tictac.init()

	
