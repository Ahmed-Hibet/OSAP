from django.urls import path
from .views import MessageCreate

urlpatterns = [
    path('messages/<int:receiver_id>/', MessageCreate.as_view()),
]
