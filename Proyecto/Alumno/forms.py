from django import forms
from .models import Solicitud, Horario

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['id_horario_club']
        labels = {
            'id_horario_club': 'Horario',
       
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_horario_club'].queryset = Horario.objects.filter(capacidad__gt=0)
        self.fields['id_horario_club'].widget.attrs.update({'class': 'form-control'})
 
