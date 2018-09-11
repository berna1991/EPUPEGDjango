from django import forms


class PostForm(forms.Form):
    usuario = forms.CharField(label = 'Usuario')
    password = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput)
