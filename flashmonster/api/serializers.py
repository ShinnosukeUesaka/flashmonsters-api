from flashmonster.api.models import AppUser, Word, Examples
from rest_framework import serializers


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'name']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'monster_image', 'monster_description', 'generated', 'learning', 'user', 'examples']
