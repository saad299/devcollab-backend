from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CollaborationRequest, Project
from .permissions import IsOwner
from .serializers import CollaborationRequestSerializer, ProjectSerializer

# Create your views here.

"""
in railway.json file
// "preDeployCommand": "python manage.py migrate",

"preDeployCommand": "python manage.py migrate && echo \"from django.contrib.auth import get_user_model; U=get_user_model(); U.objects.filter(email='admin@example.com').exists() or U.objects.create_superuser('admin', 'admin@example.com', 'yourpassword123')\" | python manage.py shell",
"""


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(is_open=True).select_related("owner__profile")

        search = self.request.query_params.get("search", "").strip()
        tech_stack = self.request.query_params.get("tech_stack", "").strip()
        role = self.request.query_params.get("role", "").strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(tech_stack__icontains=search)
            ).distinct()

        if tech_stack:
            queryset = queryset.filter(Q(tech_stack__icontains=tech_stack)).distinct()

        if role:
            queryset = queryset.filter(Q(role__icontains=role)).distinct()

        return queryset

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        if self.action == "mine":
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request):
        projects = (
            Project.objects.filter(owner=request.user)
            .select_related("owner__profile")
            .order_by("-created_at")
        )
        serializer = self.get_serializer(
            projects, many=True, context=self.get_serializer_context()
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollaborationRequestViewSet(viewsets.ViewSet):
    serializer_class = CollaborationRequestSerializer
    """
        Handles collaboration requests nested under a project
        URL: /api/projects<project_id>/requests/
    """
    def get_project(self, project_id):
        return get_object_or_404(Project, id=project_id)

    def list(self, request, project_id=None):
        project = self.get_project(project_id)

        if project.owner != request.user:
            return Response(
                {
                    "error": "You do not have permission to view collaboration requests for this project. Only the project owner can view collaboration requests."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        requests = (
            CollaborationRequest.objects.filter(project=project)
            .select_related("requester__profile")
            .order_by("-created_at")
        )
        serializer = CollaborationRequestSerializer(
            requests,
            many=True,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = self.get_project(project_id)

        if self.request.user == project.owner:
            return Response(
                {
                    'error': 'You cannot request to join your own project',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        existing = CollaborationRequest.objects.filter(
            project = project,
            requester=self.request.user
        ).first()
        
        if existing:
            return Response(
                {
                    'error': 'You have already requested to join this project',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CollaborationRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            try:
                serializer.save(project=project, requester=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {
                        'error': 'You have already requested to join this project',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update_status(self, request, project_id=None, id=None):
        project = self.get_project(project_id)

        if project.owner != self.request.user:
            return Response(
                {
                    "error": "Only the project owner can update request status"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        collaboration_request = get_object_or_404(
            CollaborationRequest,
            id=id,
            project=project
        )
        
        new_status = request.data.get('status', '').strip()

        if new_status not in ['accepted', 'rejected']:
            return Response(
                {
                    'error': 'Status must be either "accepted" or "rejected".'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        collaboration_request.status = new_status
        collaboration_request.save()

        serializer = CollaborationRequestSerializer(
            collaboration_request,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        requests = CollaborationRequest.objects.filter(
            requester=request.user
        ).select_related(
            'project',
            'project__owner'
        )
        
        serializer = CollaborationRequestSerializer(
            requests,
            many=True,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )