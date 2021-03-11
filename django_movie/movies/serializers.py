from rest_framework import serializers

from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    '''Список фильмов'''

    class Meta:
        model = Movie
        field = ("title", "tagline")