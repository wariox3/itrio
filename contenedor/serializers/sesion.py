from rest_framework import serializers
from django.contrib.sessions.models import Session

class CtnSessionSerializador(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_key', 'expire_date', 'session_data']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['session_data'] = instance.get_decoded()
        return representation              