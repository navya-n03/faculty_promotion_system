from django import forms
from django.contrib.auth.models import User
from .models import Faculty

# Form for registering a new user
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Form for faculty profile (edit or fill after login)
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            'name',
            'department',
            'current_rank',
            'years_of_experience',
            'publications',
            'conferences_attended',
            'books_published',
            'phd_completed',
            'api_score',  
        ]