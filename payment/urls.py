from django.urls import path
from .views import Deposit, Withdraw, Notify, Success, Cancel
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('deposit/', Deposit.as_view()),
    path('withdraw/', Withdraw.as_view()),
    path('notify/', csrf_exempt(Notify.as_view())),
    path('success/', Success.as_view()),
    path('cancel/', Cancel.as_view()),
    path('error/', Cancel.as_view()),
]
