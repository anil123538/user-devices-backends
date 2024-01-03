from django.contrib import admin
from device_apis.models import UserDevice

# Register your models here.
@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display=(
        "email",
        "name",
        "platform",
        "model",
        "total_storage_in_gb",
        "total_ram_in_gb",
        "os_version",
        "battery_in_mah",
        "description",
        "created_at",
        "updated_at",
        
    )
    list_filter=("name","model","platform")
    search_fields=("name","model")
    sortable_by=("created_at","total_ram_in_gb","total_storage_in_gb")

    def email(self,obj):
        return obj.user.email


