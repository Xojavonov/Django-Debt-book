
from django.urls import path
from apps.views import DebtListView, DebtCreatView, DebtFinish, DebtDeleteView, DebtUpdateView

urlpatterns = [
    path('debt-book/', DebtListView.as_view(), name='debt'),
    path('debt-save/', DebtCreatView.as_view(), name='debt-save'),
    path('debt-finish/<int:pk>', DebtFinish.as_view(), name='debt-finish'),
    path('debt-update/<int:pk>', DebtUpdateView.as_view(), name='debt-update'),
    path('debt-delete/<int:pk>', DebtDeleteView.as_view(), name='debt-delete'),
]








