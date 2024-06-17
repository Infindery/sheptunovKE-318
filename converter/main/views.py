from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from docx2pdf import convert
import os
import tempfile
import threading
import pythoncom

from .forms import *

com_lock = threading.Lock()
def index(request):
    pythoncom.CoInitialize()

    if request.method == 'POST':
        form = UploadForm(request.POST)
    else:
        form = UploadForm()

    try:
        if request.method == 'POST' and request.FILES.get('file'):
            docx_file = request.FILES['file']

            if str(docx_file).split('.')[-1] != 'docx':
                return render(request, 'main/index.html', {'form': form, 'error': 'Недопустимое расширение файла. Пожалуйста, выберите файл docx'})

            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_docx:
                temp_docx.write(docx_file.read())
                temp_docx_path = temp_docx.name

            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                temp_pdf_path = temp_pdf.name

            with com_lock:
                convert(temp_docx_path, temp_pdf_path)

            with open(temp_pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()

            os.remove(temp_docx_path)
            os.remove(temp_pdf_path)

            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{str(request.FILES['file']).split('.')[0]}.pdf"'
            return response

    finally:
        pythoncom.CoUninitialize()

    return render(request, 'main/index.html', {'form': form})

def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена')