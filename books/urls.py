from django.urls import path,include
from . import views
from .views import Bookcreateview,Bookdeleteview,Bookupdateview,Booklistview,AuthorCreateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'authors',views.AuthorViewSet)
router.register(r'books',views.BookViewSet)
router.register(r'categories',views.CategoryViewSet)

urlpatterns = [
    path('',Booklistview.as_view(), name="book_list"),
    path('authors/bookcount/', views.author_count_books, name="author_count"),
    path('authors/add/',AuthorCreateView.as_view(),name="author_create"),
    path('create/',Bookcreateview.as_view(),name="book_create"),
    path('<int:pk>/edit/',Bookupdateview.as_view(),name="book_update"),
    path('<int:pk>/delete/',Bookdeleteview.as_view(),name="book_delete"),
    path('login/', views.login_view, name="login"),
    path('logout/',views.logout_view, name="logout"),

    #api routes
    path('api/',include(router.urls)),
]
