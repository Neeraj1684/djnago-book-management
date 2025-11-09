from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.name 

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category,null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"

