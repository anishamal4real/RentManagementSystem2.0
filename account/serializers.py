from rest_framework import serializers
from .models import Tenant, Landlord, Rent

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields= '__all__'
        
class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields= '__all__'
        
class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields= '__all__'
        