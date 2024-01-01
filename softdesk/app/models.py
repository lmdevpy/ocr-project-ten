from django.db import models
from customauth.models import User


class Project(models.Model):
    TYPES = (
        ("BACK-END", "Back-End"),
        ("FRONT-END", "Front-End"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPES)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    collaborators = models.ManyToManyField(
        User, through="Collaborator", related_name="project_collaborator"
    )


class Collaborator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    PRIORITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    )

    TAG_CHOICES = (
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    )

    STATUS_CHOICES = (
        ("TO DO", "To Do"),
        ("IN PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues", blank=True, null=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TO DO")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
