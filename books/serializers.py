from rest_framework import serializers
from .models import Author,Category,Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name','bio']

class BookSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(
    #     many=True,read_only=True          -- returns whole objects of each category
    # )

    # SlugRelatedField returns only name instead of whole objects
    categories = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = "name"     # use name as the display value
    )

    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset = Category.objects.all(), write_only = True
    )

    # author = AuthorSerializer(read_only=True) -- returns whole object in api
    # added StringRelatedField for author which displays name directly instead of full objects
    author = serializers.StringRelatedField(read_only = True) 
    author_id = serializers.PrimaryKeyRelatedField(
        queryset = Author.objects.all(), write_only =True
    )
    class Meta:
        model = Book
        fields = [
            'id','title','categories','category_ids',
            'author','author_id','published_date','price'
        ]

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        author = validated_data.pop('author_id')
        book = Book.objects.create(author = author, **validated_data)
        book.categories.set(category_ids)
        return book
    
    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        author = validated_data.pop('author_id')
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        if author:
            instance.author = author
        instance.save()
        if category_ids is not None:
            instance.categories.set(category_ids)
        return instance