from django.urls import path
from .views import Deposit, Withdraw, Notify

urlpatterns = [
    path('deposit/', Deposit.as_view()),
    path('withdraw/', Withdraw.as_view()),
    path('notify/', Notify.as_view()),
]
