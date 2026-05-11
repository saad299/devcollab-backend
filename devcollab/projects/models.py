from django.db import models
from django.conf import settings

# Create your models here.


class Project(models.Model):
    STATUS_CHOICES = {
        "active": "Active",
        "completed": "Completed",
        "on_hold": "On Hold",
    }

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.TextField(help_text="Comma separated list of technologies")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_tech_stack_list(self):
        return [tech.strip() for tech in self.tech_stack.split(",")]

    def get_roles_list(self):
        return [tech.strip() for tech in self.roles_needed.split(",")]

    def __str__(self):
        return f"{self.title} by {self.owner.username}"


class CollaborationRequest(models.Model):
    STATUS_CHOICES = {
        "pending": "Pending",
        "accepted": "Accepted",
        "rejected": "Rejected",
    }

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="requests"
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_requests"
    )
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["project", "requester"]

    def __str__(self):
        return f"{self.requester.username} -> {self.project.title} ({self.status})"