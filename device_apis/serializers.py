from rest_framework import serializers
from device_apis.models import UserDevice, User
from device_apis.helper import get_user_from_token


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email"]

    def create(self, validated_data):
        user=User(first_name=validated_data["first_name"],last_name=validated_data["last_name"],
                  username=validated_data["username"],email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user

   

        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=1)
    password = serializers.CharField(max_length=100)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ["name", "platform", "model", "total_storage_in_gb", "total_ram_in_gb","os_version","battery_in_mah","description"]


def create(self,validated_data):
    device=UserDevice.objects.create(**validated_data)
    return device

def update(self,instance,validated_data):
    instance.name=validated_data.get("name")
    instance.platform=validated_data.get("platform")
    instance.model=validated_data.get("model")
    instance.total_storage_in_gb=validated_data.get("total_storage_gb")
    instance.total_ram_in_gb=validated_data.get("total_ram_in_gb")
    instance.os_version=validated_data.get("os_version")
    instance.battery_in_mah=validated_data.get("battery_in_mah")
    instance.description=validated_data.get("description")

    instance.save()
    return instance

class DeviceStatsSerializers(serializers.Serializer):
    total_device=serializers.IntegerField()
    total_users=serializers.IntegerField()
    total_ios_devices=serializers.IntegerField()
    total_android_devices=serializers.IntegerField()
    total_ios_users=serializers.IntegerField()
    total_android_users=serializers.IntegerField()
    total_windows_users=serializers.IntegerField()
    total_windows_devices=serializers.IntegerField()
    