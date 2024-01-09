from rest_framework import serializers

from .models import Project, Issue, Comment, Collaborator


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        project = Project.objects.create(**validated_data)
        Collaborator.objects.create(user=user, project=project)
        return project


class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        project_id = self.context["view"].kwargs.get("project_id")
        project_instance = Project.objects.get(pk=project_id)
        validated_data["project"] = project_instance
        issue = Issue.objects.create(**validated_data)
        return issue


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user

        issue_id = self.context["view"].kwargs.get("issue_id")
        issue_instance = Issue.objects.get(pk=issue_id)
        validated_data["issue"] = issue_instance

        comment = Comment.objects.create(**validated_data)
        return comment
