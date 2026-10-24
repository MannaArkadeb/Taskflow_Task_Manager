from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Custom user model allows adding fields like 'phone_number' later
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Member', 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # M2M relationship through a custom Membership model
    members = models.ManyToManyField(User, through='Membership', related_name='projects')

    def __str__(self):
        return self.name

class Membership(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Member', 'Member'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    STATUS_CHOICES = (
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do')
    deadline = models.DateField(null=True, blank=True, db_index=True)
    
    # Existing assigned_to
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    
    # NEW: Track which manager assigned it
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)