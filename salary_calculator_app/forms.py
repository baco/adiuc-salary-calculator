# -*- coding: utf-8 -*-

#=============================================
#
# Copyright 2012 David Racca and Matias Molina.
#
# This file is part of ADIUC Salary Calculator.
#
# ADIUC Salary Calculator is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADIUC Salary Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADIUC Salary Calculator.  If not, see 
# <http://www.gnu.org/licenses/>.
#
#=============================================

from django import forms
from models import *
import datetime

#Utilizada para filtrar datos en DEtailsForm (asignaciones familiares)
def get_concepts_asigf():
    asignaciones = AsignacionFamiliar.objects.all()
    result = list()
    for a in asignaciones:
        c = (a.concepto).title()
        result.append(c)
    return list(set(result))

class AFamiliaresForm(forms.Form):
    """Formulario con opciones específicasc opcionales."""

    asig_familiar = forms.ChoiceField(
        label=u'Asignación Familiar',
        required=False,
        choices=[(i, unicode(i)) for i in get_concepts_asigf()],
        help_text= u'Seleccione el tipo de asignación.'
    )

class CommonForm(forms.Form):
    """Formulario para el cálculo de salario docente. Contiene todos los valores
    que dependen de la persona y no de cada cargo por separado."""

    fecha = forms.DateField(
        label=u'Fecha',
        initial=datetime.date.today,
        help_text=u'Seleccione una fecha para hacer el cálculo del salario.'
    )

    antiguedad = forms.ChoiceField(
        label=u'Años de Antigüedad', 
        choices=[(i, unicode(i)) for i in 
            range(0, max(AntiguedadUniversitaria.objects.all()[AntiguedadUniversitaria.objects.count()-1].anio,
            AntiguedadPreUniversitaria.objects.all()[AntiguedadPreUniversitaria.objects.count()-1].anio)+1)
        ],
        #choices=[(i, unicode(i)) for i in range(0, 24)],
        help_text=u'Ingrese su antigüedad docente'
    )

    afiliado = forms.BooleanField(label=u'Afiliado a ADIUC', required=False)
    master = forms.BooleanField(label=u'Título de masters', required=False)
    doctorado = forms.BooleanField(label=u'Título de doctorado', required=False)

class CargoUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes universitarios."""

    cargo = forms.ModelChoiceField(
        label=u'Cargo',
        queryset=CargoUniversitario.objects.all(),
        empty_label=None,
        help_text=u'Ingrese el nombre del cargo.'
    )


class CargoPreUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes Pre-universitarios."""

    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoPreUniversitario.objects.all(), empty_label=None,
       widget=forms.Select(attrs={'onChange': 'show_horas(this)', 'onLoad':'show_horas(this)', 'onKeyUp':'this.blur();this.focus();'}),
       help_text=u'Ingrese el nombre del cargo.'
    )

    horas = forms.FloatField(label=u'Horas de trabajo', min_value=0., max_value=99., initial=1., required=True,
        widget=forms.TextInput(attrs={'maxlength':'5', 'style':'width: 50px;'}),
        help_text=u'Ingrese la cantidad de horas asociadas al cargo.'
    )

    pago_por_horas_info = forms.ChoiceField(
        required=False, 
        choices=[(unicode(c.id), unicode(c.pago_por_hora))  for c in CargoPreUniversitario.objects.all()],
        widget=forms.Select(attrs={'style':'display: none;'})
    )

