from rest_framework import serializers 
from book_library.models import Member, Author, Book, BorrowedBook


class MemberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    class Meta:
        model = Member
        fields=['username', 'first_name', 'last_name', 'email', 'phone_number','password']

    def create(self, validated_data):
        user = Member(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class Authorserializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields=['first_name', 'last_name','bio']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'created_at']


class BorrowedBookSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()  
    book = serializers.StringRelatedField()
    class Meta:
        model = BorrowedBook
        ['id', 'book', 'member', 'borrowed_at', 'returned_at'] 
