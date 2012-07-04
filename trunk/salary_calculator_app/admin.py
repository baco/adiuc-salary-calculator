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

from salary_calculator_app.models import *
from django.contrib import admin

admin.site.register(CargoUniv)
admin.site.register(TipoCargo)
admin.site.register(GarantiaSalarial)
admin.site.register(CargoPreUniv)
admin.site.register(AntiguedadUniv)
admin.site.register(AntiguedadPreUniv)
admin.site.register(Aumento)
admin.site.register(RetencionPorcentual)
admin.site.register(RetencionFija)
admin.site.register(RemuneracionPorcentual)
admin.site.register(RemuneracionFija)
