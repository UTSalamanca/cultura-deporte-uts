# Login/forms.py
from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=10, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
