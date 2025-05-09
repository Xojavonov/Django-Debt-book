import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Sum, Count, F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from redis import Redis

from DjangoProject.settings import EMAIL_HOST_USER
from apps.forms import CardModelForm, EmailForm, CodeForm, RegisterModelForm, LoginForm
from apps.models import Category, Product, Card, Order,User





class SendEmailForm(FormView):
    form_class = EmailForm
    template_name = 'login_register/send-email.html'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        code = random.randrange(10 ** 5, 10 ** 6)
        redis = Redis()
        redis.set(email, code)
        send_mail(
            subject="Verification Code !!!",
            message=f"{code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        redis.expire(email, time=timedelta(2))
        return render(self.request, 'login_register/send-code.html', context={'email': email})

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)


class CodeFormView(FormView):
    form_class = CodeForm
    template_name = 'login_register/send-code.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        return render(self.request, 'login_register/register.html', context={'email': email})

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)


class RegisterCreatView(CreateView):
    queryset = User.objects.all()
    form_class = RegisterModelForm
    template_name = 'login_register/register.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'login_register/login.html'
    success_url = reverse_lazy('organic')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
# =========================================================================
class OrganicListView(LoginRequiredMixin, ListView):
    queryset = Category.objects.all()
    template_name = 'project/main.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        all_products = list(Product.objects.all())
        data['products'] = all_products
        data['products1'] = all_products[:3]
        data['products2'] = all_products[3:6]
        data['products3'] = all_products[6:9]
        data['quantity'] = 1
        data['cards'] = Card.objects.all()
        data['total'] = Card.objects.aggregate(total=Sum(F('quantity') * F('product__price'))).get('total', 1)
        data['count_cards'] = Card.objects.aggregate(counts=Count('id')).get('counts', 0)
        return data


class CardCreatView(CreateView):
    form_class = CardModelForm
    template_name = 'project/main.html'
    success_url = reverse_lazy('organic')


class OrderSaveView(View):
    def post(self, request):
        user_ids = request.POST.getlist('id')
        order_ids = request.POST.getlist('pk')
        statuses = request.POST.getlist('status')
        total_price = request.POST.getlist('total_price')
        orders = []
        for u, o, s in zip(user_ids, order_ids, statuses):
            orders.append(Order(user_id=u, card_id=int(o), status=s,total_price=total_price))
        Order.objects.bulk_create(orders)
        return redirect('organic')








