from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins
from book_library import models
from book_library import serializers



class BookListAPIView(GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    