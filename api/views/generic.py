from django.db import models, connection
from django.db.utils import OperationalError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class PingView(APIView):
  """
  A simple view to check if the server is alive.
  It's unauthenticated and performs no actions.
  """

  def get(self, request, *args, **kwargs):
    db_connected = False
    db_error = None

    try:
      # 1. Get a database connection
      with connection.cursor() as cursor:
        # 2. Execute a simple, fast, read-only query.
        # 'SELECT 1' is standard for this.
        cursor.execute("SELECT 1")
      
      # 3. If we get here, the query was successful
      db_connected = True 
    except OperationalError as e:
      # This is the most common exception Django raises if it can't connect to the database.
      db_error = str(e)

    if db_connected:
      # Everything is OK
      return Response(
        {"status": "ok", "database": "connected"},
        status=status.HTTP_200_OK
      )
    else:
      # Database check failed, report a service error
      return Response(
        {"status": "error", "database": "disconnected", "error_message": db_error},
        status=status.HTTP_503_SERVICE_UNAVAILABLE  # 503 Service Unavailable
      )
    
