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
			var step=200
			while (tl--){

				var t=tic.squares[tl]
					tic.setsquare(t.id,'n');
			}
			tic.init()

		},	
		init: function(){
			tic.mksquares()		
			scaler.all()
			tic.addclicks()
		}	
	}// end tic 

	/** Scales the tic tac toe board to match screen size
		and makes the squares, "square"
	**/	
	var scaler={

		full:1,

		down: 0.325,	
	
		mk: function(){
			var sw=window.innerWidth
			sh=window.innerHeight
			scaler.full=sw
			if (sh < sw) {
				scaler.full=sh
			}
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
				} else{
					el.style.backgroundSize="100% 100%"
			}

		}



	}

function fetch(opick,pk){
		f=document.getElementById("fu")
		if(f){
			f.parentNode.removeChild(f)
		}
		var i=document.createElement("script")
		i.id="fu"
		i.src="/tic/js/"
		if (opick==false){	
		i.src+="tic.js"
		}else {
		i.src+=opick+"/"+pk+"/tic.js"
		}
		document.body.appendChild(i)

}





tic.init()
tic.rmclicks()
setTimeout(function(){fetch(false,false)},1500)
setTimeout(tic.addclicks,1750)

