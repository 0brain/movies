from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    """Виводить список фільмів"""
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Виводить фільм в деталях"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Додає коментар до фільму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(APIView):
    """Додавання рейтингу до фільму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """Виведення списку акторів"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Виведення детальної інформації про актора чи режисера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer