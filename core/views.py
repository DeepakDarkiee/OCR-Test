import os

import ocrmypdf
import pdfplumber
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.forms import DocumentForm
from core.models import Document, Profile

@method_decorator(login_required, name='dispatch')
class SimpleUpload(View):
    def post(self, request):
        if request.FILES["myfile"]:
            myfile = request.FILES["myfile"]
            name = request.POST["name"]
            profile = request.user.profile
            p = profile.document.create(document=myfile, name=name)
            document = profile.document.last()
            uploaded_file_url = document.document.url
            myfile = str(myfile)
            myfile_name = os.path.splitext(myfile)[0]
            ocrmypdf.ocr(
                f"./{uploaded_file_url}", f"./media/{myfile_name}_ocr.pdf", deskew=True
            )
            doc = Document.objects.filter(id=p.id)
            print(type(doc))
            pdf = pdfplumber.open(f"./media/{myfile_name}_ocr.pdf")
            page = pdf.pages[0]
            text = page.extract_text()
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

@method_decorator(login_required, name='dispatch')
class DocumentView(View):
    def get(self, request):
        profile = request.user.profile
        documents = profile.document.all()
        return render(request, "core/documents.html", {"documents": documents})

@method_decorator(login_required, name='dispatch')
class SearchResultsView(ListView):
    model = Document
    template_name = "core/documents.html"

    def get_queryset(self):
        query = self.request.GET.get("q")  # new
        object_list = Document.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return object_list
