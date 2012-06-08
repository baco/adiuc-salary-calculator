#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pdb
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

### Llena los "huecos" de las tablas de antiguedades.

# Universitarias
antunivs = AntiguedadUniv.objects.order_by('-anio')
if antunivs.count()>0:
    prev = antunivs[0]
    antunivs = AntiguedadUniv.objects.exclude(anio=prev.anio).order_by('-anio')
    for ant in antunivs:
        if ant.anio < prev.anio:
            for anio in range(ant.anio+1, prev.anio):
                new_ant = AntiguedadUniv(anio=anio, porcentaje=ant.porcentaje)
                new_ant.save()
        prev = ant

# PreUniversitarias
antunivs = AntiguedadPreUniv.objects.order_by('-anio')
if antunivs.count()>0:
    prev = antunivs[0]
    antunivs = AntiguedadPreUniv.objects.exclude(anio=prev.anio).order_by('-anio')
    for ant in antunivs:
        if ant.anio < prev.anio:
            for anio in range(ant.anio+1, prev.anio):
                new_ant = AntiguedadPreUniv(anio=anio, porcentaje=ant.porcentaje)
                new_ant.save()
        prev = ant
