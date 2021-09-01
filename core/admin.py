from django.contrib import admin

# Register your models here.
from core.models import Document, Profile

admin.site.register(Profile)
admin.site.register(Document)
