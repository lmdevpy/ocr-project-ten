from rest_framework import permissions
from .models import Collaborator, Project


# Pour gerer les collaborateurs d'un projet
class IsProjectAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return Collaborator.objects.filter(
                project_id=view.kwargs["project_id"], user_id=request.user.id
            ).exists()
        elif request.method == "POST":
            return Project.objects.filter(
                id=view.kwargs["project_id"], author_id=request.user.id
            ).exists()
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.project.author_id == request.user.id
        else:
            return False


# permettre uniquement a l'auteur de modifier ou supprimer sa resssource
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsCollaborator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return Project.objects.filter(
                id=view.kwargs["project_id"], collaborators=request.user
            ).exists()
        else:
            return True
