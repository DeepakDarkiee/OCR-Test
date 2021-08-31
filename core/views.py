import ocrmypdf
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from core.forms import DocumentForm
from core.models import Document
import os
import pdfplumber



def simple_upload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        print(myfile)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        myfile = str(myfile)
        myfile_name = os.path.splitext(myfile)[0]
        ocrmypdf.ocr(
            f"./{uploaded_file_url}", f"./media/{myfile_name}_ocr.pdf", deskew=True
        )
        pdf = pdfplumber.open(f"./media/{myfile_name}_ocr.pdf")
        page = pdf.pages[0]
        text = page.extract_text()
        print(text)
        return render(
            request,
            "core/simple_upload.html",
            {"uploaded_file_url": uploaded_file_url,'text':text},
        )
    return render(request, "core/simple_upload.html")


def model_form_upload(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = DocumentForm()
    return render(request, "core/model_form_upload.html", {"form": form})
