	//adds and removes clicks for the tic tac toe board
	var tic={

		pk:		false,

		xplayer:	'x',

		oplayer:	'o',

		 		
		klass:		'n',

		squares:	[],
	
	
		mksquares: function(){
			var wr=document.getElementById('wrap')
			tic.squares=Array.prototype.slice.call(wr.children)
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
					setTimeout(function(){fetch(el.id,tic.pk);},400)
					setTimeout(tic.addclicks,500)
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
			el.onclick=null
			cascade.frontslide(el)
		}, 
	
		reset:function(){
			tl=tic.squares.length
			while (tl--){
				var t=tic.squares[tl]
				tic.setsquare(t.id,'n')
			}
			tic.init()

		},	
		init: function(){
			tic.mksquares()		
			scaler.all()
			tic.addclicks()
			cascade.showtics()
		}	
	}// end tic 

	/** Scales the tic tac toe board to match screen size
		and makes the squares, "square"
	**/	
	var scaler={

		full:1,

		down: 0.325,	
	
		mk: function(){
			var sw=document.body.offsetWidth
			sh=document.body.offsetHeight
			scaler.full=sw
			if (sh < sw) {
				scaler.full=sh
			}
			scaler.full6
		},

		wrap: function(){
			var wr=document.getElementById('wrap')
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
	
		frontslide: function(el){
			var chunk=3.75
			o="0"
			slidein()
			function slidein(){
				o=parseFloat(o)+chunk
				el.style.backgroundSize=o+"%"
				if (o<100){
					setTimeout(slidein,cascade.swing(1-o))
				}
			}
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
					el.style.opacity="1"
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
				nodes.map(function(el){el.style.opacity=1})
			}else{
				nodes.map(function(el){el.style.opacity=0})
			}		
			var nl=nodes.length
			var step=cascade.step
			while (nl--){
				var el=nodes[nl]	
				setTimeout(cascade.cycle,step,el)
				step+=100	
			}	
		},

		reset: function(){
				setTimeout(cascade.hidetics,2100)
				setTimeout(tic.reset,3500)
		                        function force(){
                                tic.squares.map(function(el){el.style.opacity="1"}                        )
                        }
                        setTimeout(force,5000)
			    setTimeout(function(){fetch(false,false)},5500)


		}
	}



function fetch(opick,pk){
		f=document.getElementById("fu")
		if(f){
			f.parentNode.removeChild(f)
		}
		var i=document.createElement("script")
		i.id="fu"
		i.src=""
		if (!opick){	
		i.src+="tic.js"
		}else {
		i.src+=opick+"/"+pk+"/tic.js"
		}
		document.body.appendChild(i)

}





tic.init()
tic.rmclicks()
setTimeout(function(){fetch(false,false)},1500)
setTimeout(tic.addclicks,1650)

