from django.urls import path
from .views.generic import PingView

urlpatterns = [
  path('', PingView.as_view(), name="ping")
]