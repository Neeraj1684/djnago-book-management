from rest_framework import serializers
from .models import Author,Category,Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Category.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(queryset = Author.objects.all())
    class Meta:
        model = Book
        fields = '__all__'
        