from rest_framework import serializers
from webpages.models import OldQuestions

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldQuestions
        fields = '__all__'


