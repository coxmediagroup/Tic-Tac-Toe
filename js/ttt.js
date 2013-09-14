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
	moves:["zero","two","six","eight","seven","one","three","five"],
 	//if no block is needed, Hulk takes the first available move
	findmove: function(){
		var used=tictac.usedsquares.join()
		var sel=null
		if (foozie.squares.length===1 && foozie.squares[0] !="four"){
			sel="four"
			return sel			
		}	
		if (hulk.squares[0] ==="four" && hulk.squares.length===1){
				var ml=tictac.middles.length
				while(ml--){
					var mid=tictac.middles[ml]
					if (!used.match(mid)){
						sel=mid
						return sel	
					}		
				}
			}
				var i=0
				var hml=hulk.moves.length
				while (i< hml){
				if (used.match(hulk.moves[i])){
					i++				
				}else { 	
					sel= hulk.moves[i]
					return sel
				}
			}
			
	},			
			
	picksquare: function(){
	//After Celine smashed Hulk yesterday, Hulk is more aggressive at trying to win.
		if (hulk.canhulkwin()==="win"){
			return
		}else if (hulk.chkwingroups()){
			var sq=hulk.chkwingroups()
				
		}else if (hulk.chkmidgroups()){
			var sq=hulk.chkmidgroups()
				
		}else{
				 
			var sq=hulk.findmove()
					
		}
		
		tictac.setsquare(sq,hulk)
			
	
	},		
	
					
	//Hulk checks wingroups to see if a block is needed
	chkwingroups: function(){
		var wgl=tictac.wingroups.length 
		while(wgl--){
			var blk= hulk.chkforblock(tictac.wingroups[wgl])
			if (blk !="noblock"){
				var used=tictac.usedsquares.join()
				if (!used.match(blk)){
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
			if (!fs.match(wingroup[wl])) {	
				opensquares.unshift(wingroup[wl])
			}
		}		
		if (opensquares.length >1){
			opensquares=["noblock"]
		}
		return opensquares[0]	
	},
	
	chkmidgroups: function(){
		var mgl=tictac.midgroups.length 
		while(mgl--){
			var blk= hulk.chkforcorners(tictac.midgroups[mgl])
			if (blk !="nocorner"){
				var used=tictac.usedsquares.join()
				if (!used.match(blk)){
					return blk
				}
			}			
		}
	},
			
	chkforcorners: function(midgroup){
		var opensquares=[]
		var ml=midgroup.length
		var fs=foozie.squares.join()
		while (ml--){			
			if (!fs.match(midgroup[ml])) {	
				opensquares.unshift(midgroup[ml])
			}
		}		
		if (opensquares.length >1){
			opensquares=["nocorner"]
		}
		return opensquares[0]	
	},
			
	chkforwin:function(wg){
		var results=[]
		var unresults=[]
		var wl=wg.length
		var hs=hulk.squares.join()
		while(wl--){
			if (hs.match(wg[wl])){
				results.unshift(wg[wl])
			}else{
				var us=tictac.usedsquares.join()
				if (!us.match(wg[wl])){
					unresults.unshift(wg[wl])
				}			
			}
			if (results.length===2 && unresults.length===1){
				tictac.setsquare(unresults[0],hulk)
				results.unshift(unresults[0])
				tictac.rmclicks()
				tictac.highlight(results)
				return "win"
			}		
		}
	},
			
	// Calls hulk.chkwin on each wingroup to see if Hulk won.  
	canhulkwin: function(){
		var won="no"
		var wgl=tictac.wingroups.length 
		while(wgl--){
			var wg=tictac.wingroups[wgl]	
			won=hulk.chkforwin(wg)
			if( won==="win"){
				return won		
			}	
		}			
	}	
	
			
} //end hulk
		
var tictac={

		 		
	squareclass:'tictac',

	squares:[],
		
	usedsquares:[],
	
	corners:["zero","two","six","eight"],
	
	middles:["one","three","five","seven"],
	
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
	
	midgroups:[	["zero","one","three"],
			["one","two","five"],
			["three","six","seven"],
			["seven","eight","five"]
		],		
		 	
	mkclicks: function(){
		var sl=tictac.squares.length
				while(sl--){
					tictac.addclick(tictac.squares[sl])
				}	
		
	},
			
	addclick: function(el){ 
		el.onclick=function(){ 
			tictac.rmclicks()
			tictac.setsquare(this.id,foozie)
			setTimeout(hulk.picksquare,200)
			tictac.mkclicks()
		}
		
	},		
			
	rmclicks: function(el){
		var sl=tictac.squares.length
		while(sl--){
			tictac.squares[sl].onclick=null
		}	
		
	},	
	

	setsquare: function(square,player){
		var el=document.getElementById(square)
		el.className=player.name
		frontslide(el)
		tictac.usedsquares.unshift(square)
		player.squares.unshift(square)
		el.onclick=null
					
	}, 
	
	highlight: function(results){
		var rl=results.length
		while(rl--){
			var el=document.getElementById(results[rl])
			el.className +=" win"
		}
	},	
			
	resetsquare: function(square){ 
		square.className=tictac.squareclass
	},		
			
	resetboard: function(){
		var sl=tictac.squares.length
		while (sl--){		
			tictac.resetsquare(tictac.squares[sl])
			
		}
		tictac.usedsquares=[]
		foozie.squares=[]
		hulk.squares=[]
		document.title="Tic-Tac-Toe with Hulk "
		tictac.mkclicks()
		//var s=hulk.moves[Math.floor((Math.random()*hulk.moves.length))]
		//tictac.setsquare(s,hulk)
	},
	
	init: function(){
		var wrap=document.getElementById("wrap")
		tictac.squares=Array.prototype.slice.call(wrap.children)
		var ngd=document.getElementById("newgame")
		ngd.onclick=tictac.resetboard	
		tictac.resetboard()
	}
	
}// end tictac 


var swing=function( p ) {
		return 0.57 - Math.cos( p*Math.PI ) / 1.51;
	}
var frontslide=function(el){
	var chunk=2.75
	o="0"
	slidein()
	function slidein(){
		o=parseFloat(o)+chunk
		el.style.backgroundSize=o+"% 100%"	
		if (o < 100 ){
			setTimeout(slidein,swing(1-o))
		
		}	
	}


}	




tictac.init()

	
