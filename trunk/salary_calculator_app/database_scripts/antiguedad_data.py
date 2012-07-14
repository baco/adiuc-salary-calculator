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
sys.path.append(os.getcwd() + '/../')

try:
        from salary_calculator import settings
except ImportError:
        import sys
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)

from django.core.management import setup_environ
setup_environ(settings)

from salary_calculator_app.models import *

#################################
# Tabla de antiguedades para cargos Universitarios #
#################################
AntiguedadUniversitaria(
    anio=0,
    porcentaje=20.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=1,
    porcentaje=20.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=2,
    porcentaje=20.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=5,
    porcentaje=30.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=7,
    porcentaje=40.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=10,
    porcentaje=50.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=12,
    porcentaje=60.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=15,
    porcentaje=70.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=17,
    porcentaje=80.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=20,
    porcentaje=100.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=22,
    porcentaje=110.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadUniversitaria(
    anio=24,
    porcentaje=120.,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########

###################################
# Tabla de antiguedades para cargos Preuniversitarios#
###################################
AntiguedadPreUniversitaria(
    anio=1,
    porcentaje=10,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=2,
    porcentaje=15,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=5,
    porcentaje=30,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=7,
    porcentaje=40,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=10,
    porcentaje=50,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=12,
    porcentaje=60,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=15,
    porcentaje=70,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=17,
    porcentaje=80,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=20,
    porcentaje=100,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=22,
    porcentaje=110,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()
###########
AntiguedadPreUniversitaria(
    anio=24,
    porcentaje=120,
    vigencia_desde=date(2012, 1, 1),
    vigencia_hasta=date(2012, 12, 31)
).save()


### Llena los "huecos" de las tablas de antiguedades.

# Universitarias
#antunivs = AntiguedadUniversitaria.objects.order_by('-anio')
#if antunivs.count()>0:
#   prev = antunivs[0]
#    antunivs = AntiguedadUniversitaria.objects.exclude(anio=prev.anio).order_by('-anio')
#    for ant in antunivs:
  #      if ant.anio < prev.anio:
    #        for anio in range(ant.anio+1, prev.anio):
      #          new_ant = AntiguedadUniversitaria(anio=anio, porcentaje=ant.porcentaje)
        #        new_ant.save()
       # prev = ant

# PreUniversitarias
#antunivs = AntiguedadPreUniversitaria.objects.order_by('-anio')
#if antunivs.count()>0:
#    prev = antunivs[0]
#    antunivs = AntiguedadPreUniversitaria.objects.exclude(anio=prev.anio).order_by('-anio')
  #  for ant in antunivs:
    #    if ant.anio < prev.anio:
#            for anio in range(ant.anio+1, prev.anio):
#                new_ant = AntiguedadPreUniversitaria(anio=anio, porcentaje=ant.porcentaje)
#                new_ant.save()
#        prev = ant
