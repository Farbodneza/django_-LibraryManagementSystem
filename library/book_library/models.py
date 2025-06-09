from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Member(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username


class Author(Member):
    bio = models.TextField(blank=True)


class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    authors = models.ManyToManyField(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=30)
    class Meta:
        ordering = ["title"]


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.username} borrowed {self.book.title}"
