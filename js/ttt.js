		 var players=[{name:'foozie',squares:[]},{name:'hulk',squares:[]}]
		
		 var tictac={
		 
			activeplayer: players[0],
			
			switchplayer: function(){
				tictac.chkwingroups()
				if (tictac.activeplayer===players[0]){
					tictac.activeplayer=players[1]
				} else {
					tictac.activeplayer=players[0]
				}
			},	
			
			chkwingroups: function(){
				var wgl=tictac.wingroups.length 
				while(wgl--){
					var blk= tictac.chkforblock(tictac.wingroups[wgl])
					if (blk !="noblock"){
						if(tictac.usedsquares.indexOf(blk)===-1){
					   console.log(tictac.activeplayer.name+ "needs to be blocked at: "+ blk)
						}
					}
				}
			},		
			
			chkforblock: function(wingroup){
				var opensquares=[]
				var wl=wingroup.length
				while (wl--){
					if (tictac.activeplayer.squares.indexOf(wingroup[wl]) ===-1){
						opensquares.unshift(wingroup[wl])
					}
				}
						
				if (opensquares.length >1){
		
					opensquares=["noblock"]
				}
				
				return opensquares[0]	
			},			
					
			
			squareclass:'tictac',
			
			centersquare:"four",
			
			corners:["zero","two","six","eight"],
			
			usedsquares:[],
			
			mksquares: function(){
				this.squares=Array.prototype.slice.call(document.querySelectorAll('div.tictac'))
				this.squares.map(this.addclick)
			},
			
			addclick: function(el){ 
				el.onclick=function(){ 
				this.className=tictac.activeplayer.name;
				tictac.activeplayer.squares.unshift(this.id)
				tictac.usedsquares.unshift(this.id)
				this.onclick="";
				tictac.switchplayer()}
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
		 
		
			setsquare: function(square){
					var el=document.querySelector('#'+square)
					el.className=activeplayer.name
					switchplayers()
			}		
			
					
		}
	tictac.mksquares()		