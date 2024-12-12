from django import forms
from .models import ArchivoExcel

class ArchivoExcelForm(forms.ModelForm):
    # Agregar un campo para subir el archivo
    archivo = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ArchivoExcel
        fields = []  # No incluir 'documento' en fields

    def save(self, commit=True):
        instance = super().save(commit=False)
        archivo = self.cleaned_data['archivo']

        # Leer el archivo como binario
        if archivo:
            instance.documento = archivo.read()  # Asignar el contenido binario

        if commit:
            instance.save()
        return instance

