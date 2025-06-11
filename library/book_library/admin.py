from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, Author, Book, BorrowedBook

@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile Info', {'fields': ('phone_number',)}),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_returned', 'created_at')
    search_fields = ('title', 'authors__first_name', 'authors__last_name')
    list_filter = ('is_returned', 'authors')


@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'borrowed_at', 'returned_at')
    search_fields = ('book__title', 'member__username')
    list_filter = ('returned_at', 'member')