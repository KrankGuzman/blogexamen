from django import forms
from . import choices as app_choices
from . import queries as app_queries


class SignInForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Usuario', 'autocomplete': 'off'}))
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Nombres', 'autocomplete': 'off'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Apellidos', 'autocomplete': 'off'}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Correo Electronico', 'autocomplete': 'off'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'autocomplete': 'off'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'autocomplete': 'off'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("La confirmacion de contraseña no coincide")

        values = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
        return values


class LogInForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuario',
                'autocomplete': 'off'
            }
        )
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'autocomplete': 'off'
            }
        )
    )


class PostForm(forms.Form):
    title = forms.CharField(
        label='Titulo',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Titulo',
                'autocomplete': 'off'
            }
        )
    )
    text = forms.CharField(
        label="Text",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Texto',
                'autocomplete': 'off'
            }
        )
    )
    status = forms.ChoiceField(
        choices=app_choices.post_status_choices
    )
    tags = forms.MultipleChoiceField(
        choices=app_queries.get_tags_choices(),
        label='Tags',
        widget=forms.CheckboxSelectMultiple,
    )


class PostCommentForm(forms.Form):
    text = forms.CharField(
        label="Comment:",
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'placeholder': 'Texto',
            }
        )
    )
