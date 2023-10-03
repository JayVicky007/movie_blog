from django import forms
from .models import Blog, Contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact  
        fields = ['name', 'email', 'message'] 

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Perform any additional processing or validation here if needed
        if commit:
            instance.save()
        return instance

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']


