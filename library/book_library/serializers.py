from rest_framework import serializers 
from book_library.models import Member, Author, Book, BorrowedBook

class MemberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    class Meta:
        model = Member
        fields=['username', 'first_name', 'last_name', 'email', 'phone_number']


class Authorserializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields=['username', 'first_name', 'last_name', 'email', 'bio']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    class Meta:
        model = Book


class BorrowedBookSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()  
    book = serializers.StringRelatedField()
    class Meta:
        model = BorrowedBook
        ['id', 'book', 'member', 'borrowed_at', 'returned_at'] 
