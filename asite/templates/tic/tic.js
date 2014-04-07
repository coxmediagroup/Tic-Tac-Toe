var xpick="{{xpick}}";
var all={
	{% for field in form %}
	"{{field.name}}":"{{field.value}}",
	{%endfor %}
	};

tic.pk={{pk}};

{% if xpick %}
	tic.setsquare("{{xpick}}",tic.xplayer);
	tic.addclicks();
	
{% endif %}
	nNodes=document.getElementsByClassName('n');
	if (nNodes.length==0){
		tic.pk=false;
		cascade.reset();
	}	;

{% if wingroup|length == 3 %}
	{% for wg in wingroup %}
		tic.setsquare("{{wg}}"," win ");
	{% endfor %}
	tic.rmclicks()
		tic.pk=false;
	cascade.reset()
{% endif %}
	
