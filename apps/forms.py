
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField
from django.forms.models import ModelForm
from redis import Redis

from apps.models import Card, User


class CardModelForm(ModelForm):
    class Meta:
        model=Card
        fields=['quantity','product']


# =====================================


class EmailForm(Form):
    email=CharField(max_length=255)

    def clean_email(self):
        email=self.cleaned_data.get('email')
        query=User.objects.filter(email=email)
        if query.exists():
            raise ValidationError(f'{email} exists')
        return email

class CodeForm(Form):
    code=CharField(max_length=10)
    email=CharField(max_length=100)

    def clean_code(self):
        code=self.cleaned_data.get('code')
        email=self.data.get('email')
        redis=Redis(decode_responses=True)
        check_code=redis.get(email)
        if str(check_code)!=str(code):
            raise ValidationError('Password error!')
        return email


class RegisterModelForm(ModelForm):
    class Meta:
        model = User
        fields = 'first_name','last_name', 'password','email'


    def clean_email(self):
        email = self.cleaned_data.get('email')
        query = User.objects.filter(email=email)
        if query.exists():
            raise ValidationError(f'{email} exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        hash = make_password(password)
        return hash


class LoginForm(Form):
    email = CharField(max_length=100)
    password = CharField(max_length=100)

    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        query=User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError(f'{email} exists')
        user=query.first()
        if not check_password(password,user.password):
            raise ValidationError('Password error')
        self.user=user
        return super().clean()
