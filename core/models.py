from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class DocumentType(models.Model):
    type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.type


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to="documents/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DocumentManager(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    documents = models.ForeignKey(
        Document, on_delete=models.CASCADE, null=True, blank=True,related_name="documents"
    )

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    created_at = models.DateTimeField(auto_now=True)
    document_manager = GenericRelation(DocumentManager)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    created_at = models.DateTimeField(auto_now=True)
    document_manager = GenericRelation(DocumentManager)

    def __str__(self):
        return self.user.username
