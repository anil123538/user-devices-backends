from django.urls import path
import device_apis.views as api_views

urlpatterns = [
    path("", api_views.home, name="home"),
    path("register",api_views.UserRegistration.as_view(),name="register"),
    path("login",api_views.UserLogin.as_view(),name="login"),
    path("DeviceCreate",api_views.DeviceCreate.as_view(),name="DeviceCreate"),
    path("List-user-devices",api_views.DeviceUserList.as_view(),name="List_devices"),
    path("update-device/<int:device_id>",api_views.DeviceUpdate.as_view(),name="update_device"),
    path("device-detail/<int:device_id>",api_views.DeviceDetails.as_view(),name="device_details"),
    path("device-delete/<int:device_id>",api_views.DeviceDelete.as_view(),name="device_delete"),
    path("device-stats/<int:device_id>",api_views.DeviceStats.as_view(),name="device_stats"),


    
]
