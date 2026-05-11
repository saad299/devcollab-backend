from rest_framework import serializers
from .models import User, Profile

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        if len(data['password']) < 6:
            raise serializers.ValidationError({"password": "Password must be at least 6 characters long"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'avatar', 'skills', 'github_url', 'linkedin_url', 'website_url']
    
    get_skills_list = serializers.SerializerMethodField()
    
    def get_skills_list(self, obj):
        return obj.skills.split(',')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        depth = 1