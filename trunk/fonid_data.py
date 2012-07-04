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

#para correr sobre el shell
#python manage.py shell
#from salary_calculator_app import RemuneracionFija, RemuneracionRetencion

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

for v in fonid_values:
    r = RemuneracionFija(codigo="122",nombre="FONID",aplicacion='P',valor=v)
    r.save()
