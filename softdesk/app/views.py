from rest_framework import viewsets
from .models import Project, Issue, Comment, Collaborator
from rest_framework.generics import get_object_or_404, Http404
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    CollaboratorSerializer,
)
from .permissions import IsAuthor, IsProjectAuthor, IsCollaborator
from rest_framework.permissions import IsAuthenticated


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return self.queryset.filter(collaborators=self.request.user)


class CollaboratorViewSet(viewsets.ModelViewSet):
    serializer_class = CollaboratorSerializer
    queryset = Collaborator.objects.all()
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        return self.queryset.filter(
            project=project, project__collaborators=self.request.user
        )

    def retrieve(self, request, *args, **kwargs):
        # return 404
        raise Http404()

    def update(self, request, *args, **kwargs):
        raise Http404()

    def partial_update(self, request, *args, **kwargs):
        raise Http404()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor, IsCollaborator]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        return self.queryset.filter(
            project=project, project__collaborators=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor, IsCollaborator]

    def get_queryset(self):
        issue_id = self.kwargs["issue_id"]
        issue = get_object_or_404(Issue, id=issue_id)
        return self.queryset.filter(
            issue=issue, issue__project__collaborators=self.request.user
        )
