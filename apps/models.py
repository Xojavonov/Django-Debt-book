
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, CharField, ImageField, IntegerField, DecimalField, TextField, ForeignKey, CASCADE, \
    DateTimeField, EmailField
from django.db.models.enums import TextChoices


class Category(Model):
    class Meta:
        verbose_name_plural='categories'
    name=CharField(max_length=100)
    images=ImageField(upload_to='category/',default='immage')

    def __str__(self):
        return self.name

class Product(Model):
    name=CharField(max_length=100)
    price=DecimalField(max_digits=10,decimal_places=2)
    description=TextField(default='good')
    sale=DecimalField(max_digits=10,decimal_places=2)
    quantity=IntegerField(default=1)
    image=ImageField(upload_to='product/')
    category=ForeignKey('apps.Category',on_delete=CASCADE,related_name='products')

    def __str__(self):
        return self.name

class Card(Model):
    product=ForeignKey('apps.Product',on_delete=CASCADE,related_name='cards')
    quantity=IntegerField(default=1)

class Order(Model):
    class StatusType(TextChoices):
        SOLD='sold','Sold'
        NOT_SOLD='not sold','Not Sold'

    status=CharField(max_length=50,choices=StatusType,default=StatusType.NOT_SOLD)
    card=ForeignKey('apps.Card',on_delete=CASCADE,related_name='orders')
    user=ForeignKey('apps.User',on_delete=CASCADE,related_name='orders')
    total_price=DecimalField(max_digits=10,decimal_places=2)
    created_at=DateTimeField(auto_now_add=True)


# ======================================================================================

class CustomerUser(UserManager):
    def _create_user_object(self,email,password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self,  email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self,  email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomerUser()
    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []
    email = EmailField('email address', unique=True)











