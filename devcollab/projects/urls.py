from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, CollaborationRequestViewSet, MyRequestView

router = DefaultRouter()
router.register(
    prefix='projects',
    viewset=ProjectViewSet,
    basename='project'
)

# {"id":6,"username":"Saad","email":"saad@gamil.com","profile":{"id":6,"bio":null,"avatar":null,"skills":null,"github_url":null,"linkedin_url":null,"website_url":null,"location":null,"user":6}}
"""
1.
username = Saad
email = saad@gamil.com
password = ewrew@#$@1432rrew
2.
username = Saad1
email = saad1@gamil.com
password = erwETE25@$$@fdsfr
3.
username = Saad2
email = saad2@gamil.com
password =  ffwSd@#$@124:s35!#$s
4.
username = Some_User_123
email = someuser@devcollab.com
password =   devcollab_User_12345
5.
username = Some_User_456
email = some_user_again@devcollab.com
password =    devcollab_User_34567
"""

urlpatterns = [
    # Project URLs - handled by router
    # GET    /api/projects/              — list all open projects
    # POST   /api/projects/              — create a project
    # GET    /api/projects/<id>/         — retrieve a project
    # PUT    /api/projects/<id>/         — full update a project
    # PATCH  /api/projects/<id>/         — partial update a project
    # DELETE /api/projects/<id>/         — delete a project
    # GET    /api/projects/mine/         — current user's projects
    path('', include(router.urls)),

    # Collaboration Request URLs — manual, nested under projects
    # GET    /api/projects/<project_id>/requests/              — list requests (owner only)
    # POST   /api/projects/<project_id>/requests/              — send a request
    path(
        'projects/<int:project_id>/requests/',
        CollaborationRequestViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='project-requests'
    ),

    # PATCH  /api/projects/<project_id>/requests/<id>/         — accept or reject (owner only)
    path(
        'projects/<int:project_id>/requests/<int:id>/',
        CollaborationRequestViewSet.as_view({
            'patch': 'update_status'
        }),
        name='request-detail'
    ),

    # GET    /api/requests/mine/                               — current user's sent requests
    path(
        'requests/mine/',
        MyRequestView.as_view(),
        name='my-requests'
    )
]