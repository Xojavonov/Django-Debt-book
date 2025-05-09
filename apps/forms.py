from django.forms import ModelForm

from apps.models import DebtBook


class DebtModelFormCreate(ModelForm):
    class Meta:
        model = DebtBook
        fields = 'name', 'number', 'debt'


class DebtModelFormUpdate(ModelForm):
    class Meta:
        model = DebtBook
        fields = ['debt']
