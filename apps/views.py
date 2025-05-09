from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from apps.forms import DebtModelFormCreate,DebtModelFormUpdate
from apps.models import DebtBook


class DebtListView(ListView):
    queryset = DebtBook.objects.all()
    template_name = 'project/debt.html'
    context_object_name = 'debts'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['total_debt'] = DebtBook.objects.aggregate(Sum('debt')).get('debt__sum', 0)
        data['paid_count'] = DebtBook.objects.filter(status='tolandi').aggregate(Count('status')).get('status__count',
                                                                                                      0)
        data['unpaid_count'] = DebtBook.objects.filter(status='tolanmagan').aggregate(Count('status')).get(
            'status__count', 0)
        data['total_debtors'] = DebtBook.objects.aggregate(Count('id')).get('id__count', 0)
        return data


class DebtCreatView(CreateView):
    queryset = DebtBook.objects.all()
    form_class = DebtModelFormCreate
    template_name = 'project/debt.html'
    success_url = reverse_lazy('debt')




class DebtDeleteView(DeleteView):
    queryset = DebtBook.objects.all()
    template_name = 'project/debt.html'
    success_url = reverse_lazy('debt')
    pk_url_kwarg = 'pk'


class DebtFinish(View):
    def post(self, request, pk):
        DebtBook.objects.filter(pk=pk).update(status=DebtBook.StatusType.COMPLETED)
        return redirect('debt')


class DebtUpdateView(UpdateView):
    form_class = DebtModelFormUpdate
    queryset = DebtBook.objects.all()
    template_name = 'project/debt.html'
    success_url = reverse_lazy('debt')







