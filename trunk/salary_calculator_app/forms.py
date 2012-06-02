# -*- coding:utf-8 -*-

from django import forms
from models import *


class MesForm(forms.Form):
	"""Formulario para el cálculo de salario docente. Indica el mes correspondiente al cálculo."""

	aumento = forms.ModelChoiceField(label=u'aumento', queryset=Aumento.objects.all(),empty_label=None,
		help_text=u'Seleccione el mes sobre el cual calcular el salario.')


class CargoUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes universitarios."""

    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese el nombre del cargo.')
    antiguedad = forms.ModelChoiceField(label=u'Años de Antigüedad', queryset=AntiguedadUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese su antigüedad para el cargo.')
    master = forms.BooleanField(label=u'Master', required=False)
    doctorado = forms.BooleanField(label=u'Doctorado', required=False)


class CargoPreUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes Pre-universitarios."""
    
    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoPreUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese el nombre del cargo.')
    antiguedad = forms.ModelChoiceField(label=u'Años de Antigüedad', queryset=AntiguedadPreUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese su antigüedad para el cargo.')
    master = forms.BooleanField(label=u'Master', required=False)
    doctorado = forms.BooleanField(label=u'Doctorado', required=False)
    horas = forms.IntegerField(label=u'Cantidad de Horas', min_value=1, max_value=99,
        help_text=u'Ingrese la cantidad de horas asociadas al cargo.')


