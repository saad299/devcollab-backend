from dataclasses import fields
from rest_framework import serializers
from .models import CollaborationRequest, Project
from accounts.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Project
    #     fields = ['id', 'title', 'description', 'tech_stack', 'roles_needed', 'status', 'is_open', 'created_at', 'updated_at']

    owner_data = serializers.SerializerMethodField()
    tech_stack_list = serializers.SerializerMethodField()
    roles_list = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()
    project_id = serializers.IntegerField(source='id', read_only=True)

    # This validation is for frontend - comma-separated strings
    tech_stack = serializers.CharField()
    roles_needed = serializers.CharField()
    def validate_tech_stack(self, value):
        if isinstance(value, list):
            return ', '.join(value)
        return value

    def validate_roles_needed(self, value):
        if isinstance(value, list):
            return ', '.join(value)
        return value
    
    class Meta:
        model = Project
        fields = ['project_id', 'owner_data', 'title', 'description', 'tech_stack', 'roles_needed', 'tech_stack_list', 'roles_list', 'status', 'is_open', 'created_at', 'updated_at', 'request_status']
        # fields = ['project_id', 'owner_data', 'title', 'description', 'tech_stack', 'roles_needed', 'tech_stack_list', 'roles_list', 'status', 'is_open', 'created_at', 'updated_at', 'request_status']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner', 'tech_stack_list', 'roles_list', 'owner_data', 'request_status']

    def get_owner_data(self, obj):
        return UserSerializer(obj.owner).data
    
    def get_tech_stack_list(self, obj):
        return obj.get_tech_stack_list()

    def get_roles_list(self, obj):
        return obj.get_roles_list()

    def get_request_status(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        collaboration_request = CollaborationRequest.objects.filter(
            project=obj,
            requester=request.user
        ).first()
        if collaboration_request:
            return collaboration_request.status
        return None

class CollaborationRequestSerializer(serializers.ModelSerializer):
    requester_data = serializers.SerializerMethodField()
    project_detail = serializers.SerializerMethodField()

    class Meta:
        model = CollaborationRequest
        fields = '__all__'
        read_only_fields = [
            'id',
            'status',
            'created_at',
            'updated_at',
            'requester',
            'project',
            'requester_data',
            'project_detail'
        ]
        
    def get_requester_data(self, obj):
        from accounts.serializers import UserSerializer
        return UserSerializer(obj.requester).data
    
    def get_project_detail(self, obj):
        return {
            'id': obj.project.id,
            'title': obj.project.title,
            'owner_username': obj.project.owner.username,
            'tech_stack_list': obj.project.get_tech_stack_list(),
            'roles_list': obj.project.get_roles_list(),
            'status': obj.project.status,
            'is_open': obj.project.is_open,
        }