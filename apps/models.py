
from django.db.models import Model, CharField, ImageField, IntegerField, DecimalField, TextField, ForeignKey, CASCADE, \
    DateTimeField
from django.db.models.enums import TextChoices


class DebtBook(Model):
    class StatusType(TextChoices):
        DEBT = 'tolanmagan', 'Tolanmagan'
        COMPLETED = 'tolandi', 'Tolandi'

    name = CharField(max_length=255)
    number = CharField(max_length=20)
    debt = DecimalField(max_digits=10, decimal_places=2, default=1)
    status = CharField(max_length=35, choices=StatusType, default=StatusType.DEBT)
    date = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name





