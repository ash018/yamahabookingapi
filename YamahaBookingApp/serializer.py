from rest_framework import serializers

from .models import *

class RegisteredStgSerializer(serializers.ModelSerializer):
    json = serializers.SerializerMethodField('clean_json')
    class Meta:
        model = RegisteredUser
        fields = ('Id', 'UserName')

class SMSMessageOTPSerializer(serializers.ModelSerializer):
    json = serializers.SerializerMethodField('clean_json')
    class Meta:
        model = SMSMessage
        fields = ('Id', 'Email')



class FileSerializer(serializers.Serializer):
    file = serializers.FileField()




