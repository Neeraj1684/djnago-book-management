from django import forms
from .models import Book,Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','categories','author','published_date','price']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name','bio']

