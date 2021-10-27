from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_login_register),
    path('register', views.register),
    path('login', views.login),
    path('books', views.showBooks),
    path('logOut', views.logOut),
    path('book/<int:book_id>', views.decideWhatToShow),
    path('books/add', views.addBook),
    path('removeFavorite/<int:book_id>', views.removeFavorite),
    path('addFavorite/<int:book_id>', views.addFavorite),
    path('book/<int:book_id>/edit', views.editBook),
]