from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from book_library.models import Book, Member
from book_library import serializers
from django.contrib.auth import authenticate
from rest_framework import status


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = serializers.MemberSerializer




class LoginAPIView(APIView):
 
    def post(self, request, *args, **kwargs):
        serializer = serializers.MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            return Response({
                'user_id': user.pk,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Data'}, status=status.HTTP_401_UNAUTHORIZED)
    
# class LoginAPIView(generics.CreateAPIView):
#     serializer_class = serializers.MemberLoginSerializer
#     def perform_create(self, serializer):  
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#         try:
#             user = Member.objects.get(username=username)
#         except Member.DoesNotExist:
#             return Response({'Error': 'User not found'})
#         if user:
#                 user = authenticate(username=user.username, password=password)
#         return Response({'error': 'Invalid Member'}, status=status.HTTP_401_UNAUTHORIZED)


class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'slug'


