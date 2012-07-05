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


class CommonForm(forms.Form):
    """Formulario para el cálculo de salario docente. Contiene todos los valores
    que dependen de la persona y no de cada cargo por separado."""

    aumento = forms.ModelChoiceField(label=u'Período', queryset=Aumento.objects.all(),empty_label=None,
        help_text=u'Seleccione el mes sobre el cual calcular el salario.')
    antiguedad = forms.ChoiceField(label=u'Años de Antigüedad', 
        choices=[(i, unicode(i)) for i in 
            range(0, max(AntiguedadUniv.objects.all()[AntiguedadUniv.objects.count()-1].anio,
            AntiguedadPreUniv.objects.all()[AntiguedadPreUniv.objects.count()-1].anio)+1)
        ],
        help_text=u'Ingrese su antigüedad docente')
    afiliado = forms.BooleanField(label=u'Afiliado a ADIUC', required=False)

#class AntiguedadForm(forms.Form):
#    antiguedad = forms.ModelChoiceField(label=u'Años de Antigüedad', queryset=AntiguedadUniv.objects.all(), empty_label=None,
#        help_text=u'Ingrese su antigüedad para el cargo.')

class CargoUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes universitarios."""

    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoUniv.objects.all(), empty_label=None,
        help_text=u'Ingrese el nombre del cargo.')
    #antiguedad = forms.ModelChoiceField(label=u'Años de Antigüedad', queryset=AntiguedadUniv.objects.all(), empty_label=None,
    #help_text=u'Ingrese su antigüedad para el cargo.')
    master = forms.BooleanField(label=u'Master', required=False)
    doctorado = forms.BooleanField(label=u'Doctorado', required=False)


class CargoPreUnivForm(forms.Form):
    """Formulario de calculo de salario docente para docentes Pre-universitarios."""
    
    cargo = forms.ModelChoiceField(label=u'Cargo', queryset=CargoPreUniv.objects.all(), empty_label=None,
       widget=forms.Select(attrs={'onChange': 'show_horas(this)', 'onLoad':'show_horas(this)', 'onKeyUp':'this.blur();this.focus();'}),
       help_text=u'Ingrese el nombre del cargo.'
    )
    #antiguedad = forms.ModelChoiceField(label=u'Años de Antigüedad', queryset=AntiguedadPreUniv.objects.all(), empty_label=None,
    #help_text=u'Ingrese su antigüedad para el cargo.')
    master = forms.BooleanField(label=u'Master', required=False)
    doctorado = forms.BooleanField(label=u'Doctorado', required=False)
    horas = forms.FloatField(label=u'Cantidad de Horas', min_value=0., max_value=99., initial=1.,
        help_text=u'Ingrese la cantidad de horas asociadas al cargo.')
    pago_por_horas_info = forms.ChoiceField(required=False, 
        choices=[(unicode(c.id), unicode(c.pago_por_hora))  for c in CargoPreUniv.objects.all()],
        widget=forms.Select(attrs={'style':'display: none;'})
    )

