from django.urls import path
from book_library import views

urlpatterns = [
    path('Accounts/Register/', views.RegisterUserAPIView.as_view(), name = 'register_user'),
    path('Accounts/Login/', views.LoginAPIView.as_view(), name = 'login_user'),
    path('Books/', views.BookListAPIView.as_view(), name = 'books-list'),
    path('Books/<slug:slug>', views.BookDetailAPIView.as_view(), name = 'books-details'),
]