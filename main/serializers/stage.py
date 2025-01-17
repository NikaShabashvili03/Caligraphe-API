from rest_framework import serializers
from ..models import Stage, StageImage

class StageImageSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(required=False)

    class Meta:
        model = StageImage
        fields = ['url']

    def to_representation(self, instance):
         representation = super().to_representation(instance)
         if instance.url:
               representation['url'] = instance.url.url
         return representation
    
class StageSerializer(serializers.ModelSerializer):
    images = StageImageSerializer(many=True, read_only=True)

    class Meta:
        model = Stage 
        fields = ['id', 'images', 'name', 'is_completed']
