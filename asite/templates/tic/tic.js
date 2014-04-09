var xpick="{{xpick}}";

tic.pk={{pk}};

{% if xpick %}
	setTimeout(function(){  
		tic.setsquare("{{xpick}}","x");
		tic.addclicks();
	},2000);
{% endif %}
	nNodes=document.getElementsByClassName('n');
	if (nNodes.length==0){
		tic.pk=false;
		tic.reset();
	setTimeout(function(){  tic.pk=false;
                		tic.reset();
				fetch(false,false);},2500)
	}	;

{% if wingroup|length == 3 %}
	{% for wg in wingroup %}
		tic.setsquare("{{wg}}"," win ");
	{% endfor %}
	tic.rmclicks()
        setTimeout(function(){  tic.pk=false;
                                tic.reset();
                                fetch(false,false);},2000)

{% endif %}
	
