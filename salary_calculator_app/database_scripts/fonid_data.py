#!/usr/bin/env python
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

import sys
import os
import pdb
from datetime import date

sys.path.append(os.getcwd() + '/../../')

try:
        from salary_calculator import settings
except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)

from django.core.management import setup_environ
setup_environ(settings)

from salary_calculator_app.models import *

fonid_values = [
    '430',
    '189.26',
    '215',
    '257.88',
    '129',
    '430',
    '178.49',
    '184.53',
    '17.92',
    '14.33',
    '171.92',
    '161.25',
    '429.84',
    '343.84',
    '208.71',
    '215',
    '161.25',
    '213.63',
    '14.33',
    '107.50'
]

rt = None
codigo = "12/2"
nombre = "FONID"
aplicacion = 'P'
modo = 'P'
vigencia_desde = date(2012, 1, 1)
vigencia_hasta = date(2012, 12, 31)

if not RemuneracionRetencion.objects.filter(codigo=codigo, nombre=nombre, aplicacion=aplicacion, modo=modo).exists():
    rt = RemuneracionRetencion(codigo=codigo, nombre=nombre, aplicacion=aplicacion, modo=modo)
    rt.save()
else:
    rt = RemuneracionRetencion.objects.get(codigo=codigo, nombre=nombre, aplicacion=aplicacion, modo=modo)

for v in fonid_values:
    if not RemuneracionFija.objects.filter(valor=v, remuneracion=rt, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta).exists():
        r = RemuneracionFija(valor=v, remuneracion=rt, vigencia_desde=vigencia_desde, vigencia_hasta=vigencia_hasta)
        r.save()
