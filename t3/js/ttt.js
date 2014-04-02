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
	moves:["four","one","zero","three","five","two","seven","six","eight"],
 	//if no block is needed, Hulk takes the first available move
	findmove: function(){	
		var used=tictac.usedsquares
		var sel=null
/**		if (hulk.squares[0] ==="four" && hulk.squares.length===1){
				var ml=tictac.middles.length
				while(ml--){
					var mid=tictac.middles[ml]
					if (!isin(mid,used)){
						sel=mid
						return sel	
					}		
				}
		}
**/
		var i=0
		var hml=hulk.moves.length
		while (i< hml){
			if (isin(hulk.moves[i],used)){
				i++				
			}else { 	
				sel= hulk.moves[i]
				return sel
			}
		}	
	},			
			
			
	picksquare: function(){
			var sq=""
			if (hulk.canhulkwin()==="win"){
				return
			}else if (hulk.chkwingroups()){
				sq=hulk.chkwingroups()				
			}else if (hulk.chkmidgroups()){
				sq=hulk.chkmidgroups()	
			}else{
				 sq=hulk.findmove()			
			}
			tictac.setsquare(sq,hulk)
			tictac.mkclicks()	
	},		
	
					
	//Hulk checks wingroups to see if a block is needed
	chkwingroups: function(){
		var wgl=tictac.wingroups.length 
		while(wgl--){
			var blk= hulk.chkforblock(tictac.wingroups[wgl])
			if (blk !="noblock"){
				var used=tictac.usedsquares
				if (!isin(blk,used)){
					return blk
				}
			}			
		}
	},

			
	chkforblock: function(wingroup){
		var opensquares=[]
		var wl=wingroup.length
		while (wl--){			
			if (!isin(wingroup[wl],foozie.squares)) {	
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
					if (!isin(blk,tictac.usedsquares)){
						return blk
					}
				}			
			}
	},

			
	chkforcorners: function(midgroup){
			var opensquares=[]
			var ml=midgroup.length
			while (ml--){			
			if (!isin(midgroup[ml],foozie.squares)) {	
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
		while(wl--){
			if (isin(wg[wl],hulk.squares)){
				results.unshift(wg[wl])
			}else{
				
				if (!isin(wg[wl],tictac.usedsquares)){
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

	scaler:	1,
		 		
	squareclass:	'tictac',

	squares:	[],
		
	usedsquares:	[],
	
	middles:	["one","three","five","seven"],
	
				
	wingroups:	[	["zero","one","two"], 
				["three","four","five"], 
				["six","seven","eight"],
				["zero","three","six"],
				["one","four","seven"],
				["two","five","eight"], 
				["zero","four","eight"], 
				["two","four","six"]  
	],
	
	
	midgroups:	[	["zero","one","three"],
				["one","two","five"],
				["three","six","seven"],
				["seven","eight","five"]
	],		
	
		 	
	mkclicks: function(){
			var sl=tictac.squares.length
				while(sl--){
					if (!isin(tictac.squares[sl].id,tictac.usedsquares)){									tictac.addclick(tictac.squares[sl])	
					}	
				}	
	},
			
	addclick: function(el){ 
			el.onclick=function(){ 
				tictac.rmclicks()
				tictac.setsquare(this.id,foozie)
				setTimeout(hulk.picksquare,799)
			}
	},		
	
	rmclick: function(el){
			el.onclick=null
	},
		
	rmclicks: function(el){
			tictac.squares.map(tictac.rmclick)	
	},	
	
	setsquare: function(square,player){
		var el=document.getElementById(square)
		if (el){
			el.className=player.name
			frontslide(el)
			tictac.usedsquares.unshift(square)
			player.squares.unshift(square)
			el.onclick=null
		}			
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
		tictac.scalesquare(square)
	},		
	
	mkscaler: function(){
		var sw=document.querySelector('body').offsetWidth
		sh=window.innerHeight
		tictac.scaler =(sw*0.30)
		var wr=document.querySelector('#wrap')
		wr.style.width=sw+'px'
		if (sh < sw) {
		 	wr.style.width=sh+'px'
         		tictac.scaler=(sh*0.30)
		}
		wr.style.height=wr.style.width
		document.title=document.querySelector('body').offsetWidth+"height: "+document.querySelector('body').offsetHeight
	},

	scalewrap: function(){
		var wr=document.querySelector('#wrap')
		wr.style.width=(tictac.scaler*3.3)+'px'
		wr.style.height=(tictac.scaler*3.1)+'px'

	},

	scalesquare: function(square){
        	square.style.width=tictac.scaler+"px"
        	square.style.height=tictac.scaler+"px"
	},

	cleararrays: function(){
			tictac.usedsquares=[]
			foozie.squares=[]
			hulk.squares=[]
	},

	resetboard: function(){
		tictac.mkscaler()
	tictac.scalewrap()
		tictac.squares.map(tictac.resetsquare)
		tictac.cleararrays()
		tictac.mkclicks()
	},
	
	init: function(){
		tictac.squares=Array.prototype.slice.call(wrap.children)
		//var ngd=document.getElementById("newgame")
		//ngd.onclick=tictac.resetboard	
		tictac.resetboard()
	}	
}// end tictac 


var swing=function( p ) {
		return 0.57 - Math.cos( p*Math.PI ) / 1.51;
}
	
var frontslide=function(el){
	var chunk=3.75
	o="0"
	slidein()
	function slidein(){
		o=parseFloat(o)+chunk
		el.style.backgroundSize=o+"%  "	
		if (o < 100 ){
			setTimeout(slidein,swing(1-o))
		}	
	}
}	

var isin=function(avar,aray){
	var astr=aray.join()
	if (astr.match(avar)){
		return avar
	}
}		



tictac.init()

