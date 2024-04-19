from django.db import models

from django.contrib.auth.models import Permission

# Define a custom permission
my_permission = Permission.objects.create(
    codename='can_access_special_view',
    name='Can Access Special View',
    content_type=ContentType.objects.get_for_model(MyModel)
)


# Create your models here.
