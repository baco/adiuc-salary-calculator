# -*- coding:utf-8 -*-

from django import forms
from models import *

# Una forma pulenta de hacer esto es usando los 'ModelChoiceField'

#year_choices = (
#('0','0'),
#('1','1'),
#('2','2'),
#('5','5'),
#('7','7'),
#('10','10'),
#('12','12'),
#('15','15'),
#('17','17'),
#('20','20'),
#('22','22'),
#('24','24'),
#)

class CargoUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes universitarios."""

    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese el nombre del cargo.')
    antiguedad = forms.ModelChoiceField(label=u'Antigüedad', queryset=AntiguedadUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese su antigüedad para el cargo.')
    master = forms.BooleanField(label=u'¿Posee título de maestría?', required=False)
    doctorado = forms.BooleanField(label=u'¿Posee título de doctorado?', required=False)
