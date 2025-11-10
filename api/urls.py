from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.generic import PingView, MemoViewSet

router = DefaultRouter()
router.register(r'memos', MemoViewSet, basename='memo')

urlpatterns = [
  path('ping', PingView.as_view(), name="ping"),
  path('', include(router.urls)),
]
