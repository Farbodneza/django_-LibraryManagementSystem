from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from book_library.models import Book, Member,BorrowedBook
from book_library import serializers
from django.contrib.auth import logout, authenticate, login
from rest_framework import status
from django.contrib.auth.decorators import login_required


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = serializers.MemberSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    



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

@login_required
class AddBookAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


@login_required
class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    

@login_required
class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'slug'


@login_required
class BorrowBookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = serializers.BorrowedBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        books_ids = serializer.validated_data['book_ids']
        member = request.user

        successful_borrowed_books = []
        for book_id in books_ids:
            book = Book.objects.get(pk=id)
            if BorrowedBook.objects.filte(book=book, returned_at__isnull=True):
                return Response(f"Book '{book.title}' (ID: {book_id}) is currently unavailable.")

            borrowed_book = BorrowedBook.objects.create(book=book, member=member)
            book.is_returned = False
            successful_borrowed_books.append(borrowed_book)
            
        output_serializer = serializers.BorrowedBookSerializer(borrowed_book, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)



