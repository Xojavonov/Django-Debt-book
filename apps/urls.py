
from django.urls import path
from apps.views import OrganicListView, CardCreatView, OrderSaveView, RegisterCreatView, LoginFormView, SendEmailForm, \
    CodeFormView, LogoutView

urlpatterns=[
    path('organic/',OrganicListView.as_view(),name='organic'),
    path('card-save/',CardCreatView.as_view(),name='card-save'),
    path('order-save',OrderSaveView.as_view(),name='order-save')
]

urlpatterns += [
    path('register', RegisterCreatView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('',SendEmailForm.as_view(), name='email'),
    path('check-code/',CodeFormView.as_view(), name='code'),
    path('logout/', LogoutView.as_view(), name='logout')
]



