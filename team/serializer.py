from rest_framework import serializers
from playable.models import Team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['ext_id', 'name', 'image_url']
