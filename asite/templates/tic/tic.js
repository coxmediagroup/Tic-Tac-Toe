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
		cascade.reset();
		tic.pk=false;
	}	;

{% if wingroup|length == 3 %}
	{% for wg in wingroup %}
		tic.setsquare("{{wg}}"," win ");
	{% endfor %}
	tic.rmclicks()
	cascade.reset()
	tic.pk=false
{% endif %}
	
