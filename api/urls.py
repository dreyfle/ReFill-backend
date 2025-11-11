from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PingView, MemoViewSet, BrandViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'memos', MemoViewSet, basename='memo')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
  path('ping', PingView.as_view(), name="ping"),
  path('', include(router.urls)),
]
