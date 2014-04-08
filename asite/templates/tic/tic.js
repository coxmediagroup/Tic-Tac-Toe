var xpick="{{xpick}}";

tic.pk={{pk}};

var all={
	{% for key, value in mtd.items %}
    {{ key }}: {{ value }},
	{% endfor %}
	};
{% if xpick %}
	tic.setsquare("{{xpick}}","x");
	tic.addclicks();
	
{% endif %}
	nNodes=document.getElementsByClassName('n');
	if (nNodes.length==0){
		tic.pk=false;
		tic.reset();
	setTimeout(function(){  tic.pk=false;
                		tic.reset();
				fetch(false,false);},2000)
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
	
