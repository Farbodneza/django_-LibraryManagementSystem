from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from book_library.models import Book, Member,BorrowedBook,Author
from book_library import serializers
from django.contrib.auth import logout, authenticate, login
from rest_framework import status
from django.contrib.auth.decorators import login_required


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = serializers.MemberSerializer
    
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            return Response({
                'user_id': user.id,
                'username': user.username,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)


class AddBookAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'slug'


class BorrowBookAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.BorrowedBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_ids = serializer.validated_data['book_ids']
        member = request.user
        successful_borrowed_books = []

        for book_id in book_ids:
            book = get_object_or_404(Book, pk=book_id)

            if BorrowedBook.objects.filter(book=book, returned_at__isnull=True).exists():
                return Response(
                    {"error": f"Book '{book.title}' (ID: {book_id}) is currently unavailable."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            BorrowedBook.objects.create(book=book, member=member)
            book.is_returned = False
            book.save()
            successful_borrowed_books.append(book)

        output_serializer = serializers.BookSerializer(successful_borrowed_books, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class AuthorAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.Author
    lookup_field = 'slug'


