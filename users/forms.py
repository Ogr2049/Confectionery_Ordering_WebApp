from django import forms
from .models import User

class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Почта"
        self.fields["password"].label = "Пароль"
        self.fields["password"].error_messages["required"] = "Неверный пароль"

    def clean(self):
        email = self.cleaned_data["email"]
        passwrod = self.cleaned_data["password"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователя с таким Email не существует")
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(passwrod):
                raise forms.ValidationError("Неверный пароль", code="password")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ["email", "password"]

class RegistrationForm(forms.ModelForm):

    full_name = forms.CharField(required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(required=True, widget=forms.EmailInput())
    phone = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Почта"
        self.fields["password"].label = "Пароль"
        self.fields["confirm_password"].label = "Подтвердите пароль"

    def clean_email(self):
        email = self.cleaned_data["email"]
        domain = email.split(".")[-1]
        if domain in ["net"]:
            raise forms.ValidationError("Регистрация для данного домена не возможно")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Данная почта уже существует")
        return email

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError("Пароли не сопадают")
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            "password",
            "confirm_password",
            "email",
            "phone",
            "full_name",
        ]