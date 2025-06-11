from django.urls import path
from book_library import views

urlpatterns = [
    path('Accounts/Register/', views.RegisterUserAPIView.as_view(), name = 'register-user'),
    path('Accounts/Login/', views.LoginAPIView.as_view(), name = 'login-user'),
    path('Accounts/Logout/', views.LogoutAPIView.as_view(), name = 'logout-user'),

    path('Books/', views.BookListAPIView.as_view(), name = 'books-list'),
    path('Books/Add', views.AddBookAPIView.as_view(), name = 'create-book'),
    path('Books/<slug:slug>', views.BookDetailAPIView.as_view(), name = 'books-details'),
    path('Books/Borrow/', views.BorrowBookAPIView.as_view(), name = 'borrow-books'),
    path('Books/return/', views.ReturnBooksAPIView.as_view(), name = 'return-books'),

    path('Books/Authors/<slug:slug>', views.AuthorAPIView.as_view(), name = 'Author'),
]