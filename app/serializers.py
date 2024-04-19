from rest_framework import serializers
from .models import *



# class CustomUserSerializerNL(serializers.ModelSerializer):
#     class Meta:
#         model = warehouseuser
#         fields = ['companyname', 'fullname', 'email', 'password', 'phone_no', 'country', 'state', 'terms_conditions']
        
class warehouseuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = warehouseuser
        fields = '__all__'

class GeneralSerializer(serializers.ModelSerializer):
    user = warehouseuserSerializer(read_only=True)
    class Meta:
        model = warehouseuser
        fields = '__all__'

class GstdetailsSerializer(serializers.ModelSerializer):
    user = warehouseuserSerializer(read_only=True)
    class Meta:
        model = Gstdetails
        fields = '__all__'

class AdditemSerializer(serializers.ModelSerializer):
    user = warehouseuserSerializer(read_only=True)
    class Meta:
        model = Additem
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    user = warehouseuserSerializer(read_only=True)
    class Meta:
        model = Inventory
        fields = '__all__'
