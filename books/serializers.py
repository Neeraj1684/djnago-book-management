from rest_framework import serializers
from .models import Author,Category,Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many = True, read_only = True)
    author = AuthorSerializer(read_only = True)
    class Meta:
        model = Book
        fields = '__all__'
        