from django.db.models.signals import post_migrate
from django.dispatch import receiver
from . import startup

# The @receiver decorator connects our function to the signal
@receiver(post_migrate)
def run_after_migrations(sender, **kwargs):
  """
  This function is called after migrations are applied.
  """
  # We use 'sender.name' to ensure this only runs 
  # when the migrations for *this* app ('core') are applied.
  if sender.name == 'api':
    startup.create_or_get_category()