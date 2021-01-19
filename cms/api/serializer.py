############################# Required Libraries #####################
from rest_framework import serializers
from .models import Author,Content,Admin
from .backends import authentication
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#################### Author Serializer ####################
class AuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=500,write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model= Author
        fields= '__all__'

    ####### Field Level Validations #######
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password Must Min 8 length, 1 uppercase, 1 lowercase")
        elif not re.search("[a-z]", value): 
            raise serializers.ValidationError("Password Must be Min 8 length, 1 uppercase, 1 lowercase")
        elif not re.search("[A-Z]", value):
            raise serializers.ValidationError("Password Must Min 8 length, 1 uppercase, 1 lowercase")
        return value

    def validate_email(self,value):
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("Please provide valid email")

    def validate_full_name(self,value):
        res = bool(re.search(r"\s", value)) 
        if res == False:
            raise serializers.ValidationError("Full Name must contain FirstName and LastName")
        return value

    def validate_phone(self,value):
        phone = str(value)
        if len(phone) != 10:
            raise serializers.ValidationError("Phone Number must be 10 digits")
        return value

    def validate_pincode(self,value):
        pincode = str(value)
        if len(pincode) != 6:
            raise serializers.ValidationError("pincode must be 6 digits")
        return value

    def create(self, validated_data):
        return Author.objects.create_user(**validated_data)

############ Conten Serializer #################
class ContentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Content
        fields = ['id','title','email','body','summary','document','categories']

    def create(self, validated_data):
        return Content.objects.create(**validated_data)

################ Admin Serializer ########################
class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=500,write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model= Admin
        fields= '__all__'

    def create(self, validated_data):
        return Admin.objects.create_user(**validated_data)
