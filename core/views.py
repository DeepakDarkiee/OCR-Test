import os

import ocrmypdf
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView

from core.forms import DocumentForm
from core.models import Document, DocumentManager, Profile
from core.utils import open_pdf


@method_decorator(login_required, name="dispatch")
class SimpleUpload(View):
    def post(self, request):
        if request.FILES["myfile"]:
            myfile = request.FILES["myfile"]
            name = request.POST["name"]
            try:
                user = request.user.profile
            except ObjectDoesNotExist:
                pass
            try:
                user = request.user.company
            except ObjectDoesNotExist:
                pass
            document = Document.objects.create(name=name, document=myfile)
            user.document_manager.create(documents=document)
            uploaded_file_url = document.document.url
            original_pdf = open_pdf(f"./{uploaded_file_url}")
            myfile = str(myfile)
            myfile_name = os.path.splitext(myfile)[0]
            text = original_pdf
            doc = Document.objects.filter(id=document.id)
            doc.update(description=text)
            if original_pdf is None:
                ocrmypdf.ocr(
                    f"./{uploaded_file_url}",
                    f"./media/{myfile_name}_ocr.pdf",
                    deskew=True,
                )
                doc = Document.objects.filter(id=document.id)
                text = open_pdf(f"./media/{myfile_name}_ocr.pdf")
                doc.update(document=f"./{myfile_name}_ocr.pdf", description=text)
            return render(
                request,
                "core/simple_upload.html",
                {
                    "uploaded_file_url": uploaded_file_url,
                    "text": text,
                },
            )

    def get(self, request):
        return render(request, "core/simple_upload.html")

@method_decorator(login_required, name="dispatch")
class DocumentView(View):
    def get(self, request):
        company = None
        profile = None
        try:
            profile = request.user.profile
        except ObjectDoesNotExist:
            pass

        try:
            company = request.user.company
        except ObjectDoesNotExist:
            pass
        if profile is not None:
            documents_list = []
            documents = profile.document_manager.all()
            for document in documents:
                print(document.documents)
                documents_list.append(document.documents)
            print(documents_list)
            return render(request, "core/documents.html", {"documents": documents_list})

        if company is not None:
            documents_list = []
            documents = company.document_manager.all()
            for document in documents:
                print(document.documents)
                documents_list.append(document.documents)
            print(documents_list)
            return render(request, "core/documents.html", {"documents": documents_list})
        return render(request, "core/documents.html")


@method_decorator(login_required, name="dispatch")
class SearchResultsView(ListView):
    model = Document
    template_name = "core/documents.html"

    def get_queryset(self):
        query = self.request.GET.get("q")  # new
        object_list = Document.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return object_list
