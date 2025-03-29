from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()

def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(c.isupper() for c in value):
        raise ValidationError(
            "Password must contain at least one uppercase letter.")
    if not any(c.isdigit() for c in value):
        raise ValidationError("Password must contain at least one digit.")


class ResetPasswordSerializer(serializers.ModelSerializer):
    '''
    used to verify both the password given by user is same or not 
    '''
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('password', 'confirm_password')

    def validate(self, attrs):
        user = self.context['request'].user
        if len(attrs['password']) < 8:
            raise serializers.ValidationError(
                {"len": "Password must be at least 8 characters long."})
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        elif user.check_password(attrs['password']):
            raise serializers.ValidationError(
                {"old_password": "New password cannot be same as old password"})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ChangePasswordSerializer(ResetPasswordSerializer):
    '''
    used to change password of authorised user after some validations
    '''
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value
    

class Logoutserializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        max_length=500, allow_null=False, required=True)
    
class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
