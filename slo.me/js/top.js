	var fu=''

	document.body.onload=function(){fu=document.getElementById("fuframe").contentDocument.forms[0];console.log(fu[0].value)})

	var fuform=window.frames['fuframe'].contentDocument.forms[0]
	var fu=window.frames['fuframe']
	//adds and removes clicks for the tic tac toe board
	var tic={

		xplayer:	'x',

		oplayer:	'o',
		 		
		klass:		'n',

		squares:	[],
	
	
		mksquares: function(){
			var ticnodes=document.querySelectorAll('#wrap div')
			tic.squares=Array.prototype.slice.call(ticnodes)
		},	
		
		addclicks: function(){
			tic.squares.map(tic.addclick)
		},
			
		addclick: function(el){ 
				if (el.className===tic.klass){
				el.onclick=function(e){
					e.preventDefault() 
					tic.rmclicks()
					tic.setsquare(this.id,tic.oplayer)
					fuform.submit()
					return false
				}
			}	
		},		
	
		rmclick: function(el){
				el.onclick=null
		},
		
		rmclicks: function(el){
			tic.squares.map(tic.rmclick)	
		},	
	
		setsquare: function(square,xo){
			var el=document.getElementById(square)	
			el.className=xo
			var elcid=fuform[el.id]
			elcid.value=xo
			el.onclick=null
						
		}, 
	
		reset:function(){
			//cascade.all(tic.squares,'out')
			tl=tic.squares.length
			while (tl--){
				var t=tic.squares[tl]
				tic.setsquare(t.id,'n')
			}
			tic.init()

		},	
		init: function(){
			tic.mksquares()		
			tic.addclicks()
			scaler.all()
		}	
	}// end tic 

	/** Scales the tic tac toe board to match screen size
		and makes the squares, "square"
	**/	
	var scaler={

		full:1,

		down: 0.27,	
	
		mk: function(){
			var sw=document.querySelector('body').offsetWidth
			sh=window.innerHeight
			scaler.full=sw
			if (sh < sw) {
				scaler.full=sh
			}
		},

		wrap: function(){
			var wr=document.querySelector('#wrap')
			wr.style.width=scaler.full +'px'
			wr.style.height=wr.style.width

		},

		tic: function(tic){
	        	tscale=(scaler.full*scaler.down)+"px"
	        	tic.style.height=tscale
			tic.style.width=tscale
		},


		all: function(){
			scaler.mk()
			scaler.wrap()
			var rtic=tic.squares.reverse()
			rtic.map(scaler.tic)
		}	
	}

		//Fades in the tic tac toe board
	var cascade={
	
		step: 200,
		chunk:0.01,

		swing: function( p ) {
			return 0.57 - Math.cos( p*Math.PI ) / 1.7;
		},
	
		cycle: function(el){
			 
			        var o=1.0

       				 if (el.style.opacity>0.99 ){
               				 fadeout()
       				 }else{
               				 o=0.0
               				 fadein()
       				 }

	       		 function fadeout(){
	
        	        	o=parseFloat(o)-cascade.chunk
               			el.style.opacity=o
                		if (o > 0 ){
                        		setTimeout(fadeout,cascade.swing(1-o))
               			 }else {
                        		el.style.opacity=0.0
                        		return 0
                		}
       		 	}

			function fadein(){
				o=parseFloat(o)+cascade.chunk
				el.style.opacity=o	
				if (o < 1 ){
					setTimeout(fadein,cascade.swing(1-o))
				}else {
					el.style.opacity=1
					return 0
				}	
			}
		},	

		hidetics: function(){
				
				cascade.all(tic.squares.reverse(),'out')
		},

		showtics: function(){
				cascade.all(tic.squares,'in')
		},	
		all: function(nodes,inout){
			
			if (inout=='out'){	
				nodes.map(function(el){el.style.opacity="1"})
			}else{
				nodes.map(function(el){el.style.opacity="0"})
			}		
			var nl=nodes.length
			var step=cascade.step
			while (nl--){
				var el=nodes[nl]	
				console.log(el.style.opacity)
				setTimeout(cascade.cycle,step,el)
				step+=100	
			}	
		},

		reset: function(){
				setTimeout(cascade.hidetics,1100)
				setTimeout(cascade.showtics,4200)
				setTimeout(tic.reset,3500)
		}
	}
	console.log(fu.contentDocument.innerHTML)
	
