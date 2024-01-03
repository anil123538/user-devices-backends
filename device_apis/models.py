from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    total_storage_in_gb = models.IntegerField()
    total_ram_in_gb = models.IntegerField()
    os_version = models.CharField(max_length=100)
    battery_in_mah = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

