from django import forms

class ImportarDadosForm(forms.Form):
    arquivo = forms.FileField()