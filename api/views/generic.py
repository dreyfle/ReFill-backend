from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Memo, Brand
from ..serializers import MemoSerializer, BrandSerializer


class PingView(APIView):
  """
  A simple view to check if the backend server is alive.
  It's unauthenticated and performs no actions.
  """

  def get(self, request, *args, **kwargs):
    return Response(
      {"status": "ok", "server": "running"},
      status=status.HTTP_200_OK
    )


class BrandViewSet(viewsets.ModelViewSet):
  """
  Viewset for viewing and editing Memos
  """
  serializer_class = BrandSerializer
  queryset = Brand.objects.all().order_by('name')


class MemoViewSet(viewsets.ModelViewSet):
  """
  Viewset for viewing and editing Memos
  """
  # getting all the Memos and it is sorted by its Date/Time Last Updated, where the latest Memo is first 
  queryset = Memo.objects.all().order_by('-datetime_lastupdated')
  serializer_class = MemoSerializer

  def perform_create(self, serializer):
    instance = serializer.save()

    instance.datetime_lastupdated = instance.datetime_created
    instance.save(update_fields=['datetime_lastupdated'])

  def perform_update(self, serializer):
    serializer.save(datetime_lastupdated=timezone.now())