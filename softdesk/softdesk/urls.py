"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import DefaultRouter
from app.views import ProjectViewSet, IssueViewSet, CommentViewSet, CollaboratorViewSet
from customauth.views import UserViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"projects/(?P<project_id>\d+)/collaborators", CollaboratorViewSet)
router.register(
    r"projects/(?P<project_id>\d+)/issues", IssueViewSet, basename="project-issues"
)
router.register(
    r"projects/(?P<project_id>\d+)/issues/(?P<issue_id>\d+)/comments",
    CommentViewSet,
    basename="issue-comments",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", UserViewSet.as_view({"post": "create", "get": "list"}), name="user-signup"),
]

urlpatterns += router.urls
