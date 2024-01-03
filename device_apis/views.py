import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from device_apis.helper import get_user_from_token
from device_apis.models import UserDevice
import device_apis.serializers as api_serializers
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken



# Create your views here.

@api_view(["GET"])
@permission_classes(IsAuthenticated)
def home(request):
    return Response({"message": "Welcome to device server"}, status=status.HTTP_200_OK)


class UserRegistration(generics.GenericAPIView):
    serializer_class = api_serializers.UserRegisterSerializer


    @swagger_auto_schema(tags=["user"],operation_summary="User registration")
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
            #save user
               user=serializer.create(validated_data=serializer.validated_data)
               return Response({"message":"User created sucessfully","userId":user.pk},status=status.HTTP_201_CREATED)
            print("serializer.errors ", serializer.errors)
           
            return Response({"message": "User creation failed", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception in UserRegistration:",e)
            return Response({"message":"User creation failed","errors":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





class UserLogin(generics.GenericAPIView):
    serializer_class = api_serializers.UserLoginSerializer


    @swagger_auto_schema(tags=["user"],operation_summary="User login")
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
            #save user
               user=authenticate(username=serializer.validated_data["username"],
                                 password=serializer.validated_data["password"])
               if user:
                   token=AccessToken.for_user(user)
                   return Response({"message":"User login sucessfully","token":str(token)},
                                   status=status.HTTP_200_OK)
               else:
                    return Response({"message": "User login failed", "errors": "Invalid user crendentials"},
                        status=status.HTTP_400_BAD_REQUEST)

              
           
            return Response({"message": "User login failed", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception in UserRegistration:",e)
            return Response({"message":"User login failed","errors":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class DeviceCreate(generics.GenericAPIView):
    serializer_class=api_serializers.DeviceSerializer
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(tags=["Devices"],operation_summary="Create device")
    def post(self,request):
        try:
            user_obj=get_user_from_token(request)
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.validated_data["user_id"]=user_obj.pk
                device=serializer.create(validated_data=serializer.validated_data)
                return Response({"message":"DEvice creation failed",
                                "errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception in DeviceCreate:",e)
            return Response({"message":"User login failed","errors":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class DeviceUserList(generics.GenericAPIView):
    serializer_class=api_serializers.DeviceSerializer
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(tags=["Devices"],operation_summary="Get all user devices")
    def post(self,request):
        try:
            user_obj=get_user_from_token(request)
            devices=UserDevice.objects.filter(user_id=user_obj.pk)
            serializer=self.serializer_class(devices,many=True)
            
        
            return Response({"message":"Device LIst","userId":user_obj.pk,"data":serializer.data}
                                ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception in DeviceUserList:",e)
            return Response({"message":"Internal server error","errors":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeviceUpdate(generics.GenericAPIView):
    """
    This API will update the device details
    """
    serializer_class = api_serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Devices"], operation_summary="Update device")
    def put(self, request, device_id):
        try:
            user_obj = get_user_from_token(request)
            device = UserDevice.objects.get(user_id=user_obj.pk, id=device_id)
            device_data = {
                "name": request.data.get("name", device.name),
                "platform": request.data.get("platform", device.platform),
                "model": request.data.get("model", device.model),
                "total_storage_in_gb": request.data.get("total_storage_in_gb", device.total_storage_in_gb),
                "total_ram_in_gb": request.data.get("total_ram_in_gb", device.total_ram_in_gb),
                "os_version": request.data.get("os_version", device.os_version),
                "battery_in_mah": request.data.get("battery_in_mah", device.battery_in_mah),
                "description": request.data.get("description", device.description),
                "updated_at": datetime.datetime.now()
            }
            serializer = self.serializer_class(data=device_data)
            if serializer.is_valid(raise_exception=True):
                serializer.update(instance=device, validated_data=serializer.validated_data)
                return Response({"message": "Device updated successfully",
                                 "deviceId": device_id,
                                 "data": serializer.data},
                                status=status.HTTP_200_OK)
            return Response({"message": "Device update failed",
                             "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except UserDevice.DoesNotExist:
            return Response({"message": "Device not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Exception in DeviceUpdate: ", e)
            return Response({"message": "Internal server error",
                             "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeviceDetails(generics.GenericAPIView):
    serializer_class=api_serializers.DeviceSerializer
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(tags=["Devices"],operation_summary="Get  device details")
    def post(self,request,device_id):
        try:
            user_obj=get_user_from_token(request)
            devices=UserDevice.objects.get(user_id=user_obj.pk)
            device_data=self.serializer_class(devices).data
            
        
            return Response({"message":"Device details","userId":user_obj.pk,"data":device_data}
                                ,status=status.HTTP_200_OK)
        except UserDevice.DoesNotExist:
           
            return Response({"message":"Internal server error","errors":str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeviceDelete(generics.GenericAPIView):
    serializer_class=api_serializers.DeviceSerializer
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(tags=["Devices"],operation_summary="device delete")
    def delete(self,request,device_id):
        try:
            user_obj=get_user_from_token(request)
            devices=UserDevice.objects.get(user_id=user_obj.pk).delete()
            device_data=self.serializer_class(devices).data
            
        
            return Response({"message":"Device delete","userId":user_obj.pk,"deviceId":device_id}
                                ,status=status.HTTP_200_OK)
        except UserDevice.DoesNotExist:
           
            return Response({"message":"Device not found",},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception in DeviceDelete: ", e)
            return Response({"message": "Internal server error",
                             "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        


class DeviceStats(generics.GenericAPIView):
    """
    This API will return the device stats
    """
    permission_classes = [IsAuthenticated]
    serializer_class = api_serializers.DeviceStatsSerializers

    @swagger_auto_schema(tags=["Devices"], operation_summary="Get device stats")
    def get(self, request):
        try:
            user_obj = get_user_from_token(request)
            device_stats = {
                "total_devices": UserDevice.objects.all().count(),
                "total_users": UserDevice.objects.all().count(),
                "total_android_devices": UserDevice.objects.filter(platform__icontains="Android").count(),
                "total_ios_devices": UserDevice.objects.filter(platform__icontains="iOS").count(),
                "total_android_users": UserDevice.objects.filter(platform__icontains="Android").values("user_id").distinct().count(),
                "total_ios_users": UserDevice.objects.filter(platform__icontains="iOS").values("user_id").distinct().count(),
                "total_windows_devices": UserDevice.objects.filter(platform__icontains="Windows").count(),
                "total_windows_users": UserDevice.objects.filter(platform__icontains="Windows").values("user_id").distinct().count()
            }
            return Response({"userId": user_obj.pk,
                             "data": device_stats},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception in DeviceStat: ", e)
            return Response({"message": "Internal server error",
                             "errors": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
