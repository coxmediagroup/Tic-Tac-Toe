from django.forms import widgets
from rest_framework import serializers

class BoardSerializer(serializers.Serializer):
	"""
	Responsible for Serializing and De-Serializing a Game Board.
	"""
	pk = serializers.Field()

	# Top Row
	top_left = serializers.IntegerField()
	top_center = serializers.IntegerField()
	top_right = serializers.IntegerField() 

	# Center Row
	left = serializers.IntegerField()
	center = serializers.IntegerField()
	right = serializers.IntegerField()

	# Bottom Row
	bottom_left = serializers.IntegerField()
	bottom_center = serializers.IntegerField()
	bottom_right = serializers.IntegerField()

	