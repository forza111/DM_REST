from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db import models


from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    '''Вывод списка фильмов'''
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(
                ratings__ip=get_client_ip(self.request)))
            ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) /
                        models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    '''Вывод фильма'''
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(APIView):
    '''Добавление отзыва к фильму'''
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    '''Добавление рейтинга фильму'''
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    '''Вывод списка актеров'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    '''Вывод актера или режиссера'''
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer