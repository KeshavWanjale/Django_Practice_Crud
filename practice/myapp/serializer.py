from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # this will properly transfer our data into JSON  format
    class Meta:
        model = User
        fields = '__all__'