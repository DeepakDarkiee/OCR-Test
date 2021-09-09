from django.contrib import admin

# Register your models here.
from core.models import Company, Document, DocumentManager, Profile

admin.site.register(Profile)
admin.site.register(Document)
admin.site.register(DocumentManager)
admin.site.register(Company)
