from django import forms

class BlogImportForm(forms.Form):
    csv_file = forms.FileField()
