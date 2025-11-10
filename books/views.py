from django.shortcuts import render,redirect
from django.db.models import Count,Q
from .models import Book,Author,Category
from django.views.generic import CreateView,UpdateView,DeleteView,ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import BookForm
from django.contrib.auth import login,authenticate,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#DRF IMPORTS -----
from rest_framework import viewsets
from .serializers import CategorySerializer,BookSerializer,AuthorSerializer


# Create your views here.

# def book_list(request):
#     author_name = request.GET.get('author')

#     books = Book.objects.select_related('author','category').all()

#     if author_name:
#         books = books.filter(author__name__icontains = author_name)

#     return render(request, 'books/book_list.html', {'books' : books})

def author_count_books(request):
    authors = Author.objects.annotate(book_count = Count('book'))
    return render(request, 'books/author_count.html', {'authors':authors})

class AuthorCreateView(CreateView):
    model = Author
    fields = ['name','bio']
    template_name = 'books/author_form.html'
    success_url = reverse_lazy('book_list')

@method_decorator(login_required, name="dispatch")
class Booklistview(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    ordering = ['title']
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        qs = super().get_queryset().select_related('author')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(price__icontains=query) |
                Q(published_date__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()
        return qs

@method_decorator(login_required, name="dispatch")
class Bookcreateview(CreateView):
    model = Book
    form_class = BookForm
    # fields = ['title','categories','author','published_date','price']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

@method_decorator(login_required, name="dispatch")
class Bookupdateview(UpdateView):
    model = Book
    form_class = BookForm
    # fields = ['title','categories','author','published_date','price']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

@method_decorator(login_required, name="dispatch")
class Bookdeleteview(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('book_list')
        else:
            return render(request, "books/login.html", {'error':'Invalid Credentials'})
    return render(request, 'books/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# DRF API views
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer