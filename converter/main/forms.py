from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(required=False, label="Файл")