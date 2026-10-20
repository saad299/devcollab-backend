from django.urls import path
from . import views

urlpatterns = [

    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),

    # profile
    path('users/me/', views.ProfileView.as_view(), name='profile'),
    path('users/<str:username>/', views.PublicProfileView.as_view(), name='public_profile'),
]