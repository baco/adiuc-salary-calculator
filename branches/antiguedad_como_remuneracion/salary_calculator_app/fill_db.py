#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
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


#=============================================#
#						CARGOS UNIVERSITARIOS												  #
#=============================================#
c = Cargo(lu='5', pampa='101', tipo='Profesor Titular D.E', basico=6831.76)
c.save()
c = Cargo(lu='13', pampa='102', tipo='Profesor Titular D.S.E', basico=3415.88)
c.save()
c = Cargo(lu='27', pampa='103', tipo='Profesor Titular D.S', basico=1707.94)
c.save()
c = Cargo(lu='6', pampa='105', tipo='Profesor Asociado D.E', basico=6146.54)
c.save()
c = Cargo(lu='8', pampa='106', tipo='Profesor Asociado D.S.E', basico=3073.27)
c.save()

# TODO: Complete with the rest of the teaching positions

os.system('python ../manage.py dumpdata --indent=2 > db_dump.json')
