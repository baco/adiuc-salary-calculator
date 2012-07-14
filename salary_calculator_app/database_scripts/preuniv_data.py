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
#						CARGOS PREUNIVERSITARIOS											   #
#=============================================#

def add_cargo_preuniv(nombre, lu, pampa, basico_unc, basico_nac, horas, tipo_horas, pago_por_hora):
    """Agrega un cargo pre univ a la BD."""

    if TipoCargo.objects.filter(nombre=nombre).exists():
        t = TipoCargo.objects.get(nombre=nombre)
    else:
        t = TipoCargo(nombre=nombre)
        t.save()
    
    c = None
    if CargoPreUniv.objects.filter(
        lu=lu,
        pampa=pampa,
        tipo=t,
        basico_unc=basico_unc,
        basico_nac=basico_nac,
        horas=horas,
        tipo_horas=tipo_horas,
        pago_por_hora=pago_por_hora
    ).exists():
        c = CargoPreUniv.objects.get(
            lu=lu,
            pampa=pampa,
            tipo=t,
            basico_unc=basico_unc,
            basico_nac=basico_nac,
            horas=horas,
            tipo_horas=tipo_horas,
            pago_por_hora=pago_por_hora
        )
    else:
        c = CargoPreUniv(
            lu=lu,
            pampa=pampa,
            tipo=t,
            basico_unc=basico_unc,
            basico_nac=basico_nac,
            horas=horas,
            tipo_horas=tipo_horas,
            pago_por_hora=pago_por_hora
        )
        c.save()

    if c:
        for rem in RemuneracionPorcentual.objects.filter(aplicacion='P'):
            c.rem_porcentuales.add(rem)
        for rem in RemuneracionPorcentual.objects.filter(aplicacion='T'):
            c.rem_porcentuales.add(rem)
        for ret in RetencionPorcentual.objects.filter(aplicacion='P'):
            c.ret_porcentuales.add(ret)
        for ret in RetencionPorcentual.objects.filter(aplicacion='T'):
            c.ret_porcentuales.add(ret)

    return c


def add_garantia_preuniv(cargo, valor, mes, anio):
    """Crea una garantia salarial nueva si no existia ya en la BD con los 
    valores dados y la asocia al cargo que toma por parametro."""
    if GarantiaSalarial.objects.filter(valor=valor, mes=mes, anio=anio).exists():
        g = GarantiaSalarial.objects.get(valor=valor, mes=mes, anio=anio)
    else:
        g = GarantiaSalarial(valor=valor, mes=mes, anio=anio)
        g.save()
    cargo.garantia_salarial.add(g)


# Base: Copiar y pegar este
###############
#c = add_cargo_preuniv(
#    nombre = u'', 
#    lu = u'', 
#    pampa = u'', 
#    basico_unc = , 
#    basico_nac = , 
#    horas = , 
#    tipo_horas = '',
#    pago_por_hora = False
#)
#add_garantia_preuniv(
#    cargo = c,
#    valor = ,
#    mes = 'MAR',
#    anio = '2012'
#)
#add_garantia_preuniv(
#    cargo = c,
#    valor = ,
#    mes = 'JUN',
#    anio = '2012'
#)

##############
c = add_cargo_preuniv(
    nombre = u'Vice Director de 1°', 
    lu = u'1', 
    pampa = u'201', 
    basico_unc = 5079.6, 
    basico_nac = 5079.6, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
##############
c = add_cargo_preuniv(
    nombre = u'Regente de 1°', 
    lu = u'2', 
    pampa = u'202', 
    basico_unc = 4830.76, 
    basico_nac = 4830.76, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
##############
c = add_cargo_preuniv(
    nombre = u'Jefe Gral Ens.Práctica', 
    lu = u'3', 
    pampa = u'203', 
    basico_unc = 4442.50, 
    basico_nac = 4442.50, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2464.76,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2464.76,
    mes = 'JUN',
    anio = '2012'
)
##############
c = add_cargo_preuniv(
    nombre = u'Profesor TC', 
    lu = u'4', 
    pampa = u'204', 
    basico_unc = 6092.64, 
    basico_nac = 6092.64, 
    horas = 36, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Asesor Pedagógico', 
    lu = u'10', 
    pampa = u'205', 
    basico_unc = 6092.64, 
    basico_nac = 6092.64, 
    horas = 36, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Labor. Informática', 
    lu = u'11', 
    pampa = u'206', 
    basico_unc = 3427, 
    basico_nac = 3427, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Asesor Psicopedagógico', 
    lu = u'12', 
    pampa = u'207', 
    basico_unc = 3046.32, 
    basico_nac = 3046.32, 
    horas = 18, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 3358.47,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 3358.47,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Director Escuela Superior', 
    lu = u'15', 
    pampa = u'208', 
    basico_unc = 2445.48, 
    basico_nac = 2445.48, 
    horas = 35, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Clases Práct.(02)', 
    lu = u'16', 
    pampa = u'209', 
    basico_unc = 1988.915, 
    basico_nac = 1988.915, 
    horas = 12, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 1680,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 1680,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Vice Director Escuela Superior', 
    lu = u'17', 
    pampa = u'210', 
    basico_unc = 2306.97, 
    basico_nac = 2306.97, 
    horas = 35, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Rector de 1° Categoría', 
    lu = u'18', 
    pampa = u'211', 
    basico_unc = 5394.5, 
    basico_nac = 5394.5, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Clases Prácticas', 
    lu = u'19', 
    pampa = u'212', 
    basico_unc = 1749.7, 
    basico_nac = 1749.7, 
    horas = 21, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Director de 3° Categoría', 
    lu = u'21', 
    pampa = u'213', 
    basico_unc = 1994.97, 
    basico_nac = 1994.97, 
    horas = 35, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prosecretario 1° (Esc.Com.)', 
    lu = u'22', 
    pampa = u'240', 
    basico_unc = 3300.25, 
    basico_nac = 3300.25, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de Esc.Superior', 
    lu = u'23', 
    pampa = u'214', 
    basico_unc = 3290.75, 
    basico_nac = 3290.75, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de 1° Esc.Superior', 
    lu = u'24', 
    pampa = u'215', 
    basico_unc = 2219.31, 
    basico_nac = 2219.31, 
    horas = 35, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Secret. de 1° Categoría', 
    lu = u'25', 
    pampa = u'216', 
    basico_unc = 1786.14, 
    basico_nac = 1786.14, 
    horas = 35, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Secretario Esc.Superior', 
    lu = u'29', 
    pampa = u'217', 
    basico_unc = 3617.5, 
    basico_nac = 3617.5, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. Jefe Trab.Prácticos', 
    lu = u'30', 
    pampa = u'218', 
    basico_unc = 1769.2, 
    basico_nac = 1769.2, 
    horas = 21, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Bibliot. Ley 22.416', 
    lu = u'33', 
    pampa = u'219', 
    basico_unc = 2430.973, 
    basico_nac = 2430.973, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2324.51,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2324.51,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. Jefe Trab.Prácticos', 
    lu = u'35', 
    pampa = u'220', 
    basico_unc = 1769.2, 
    basico_nac = 1769.2, 
    horas = 21, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. Centro Deportivo', 
    lu = u'37', 
    pampa = u'221', 
    basico_unc = 1621.95, 
    basico_nac = 1621.95, 
    horas = 17, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Maestro Ayud.Ens.Práctico', 
    lu = u'38', 
    pampa = u'222', 
    basico_unc = 1497.01, 
    basico_nac = 1497.01, 
    horas = 18, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Preceptores de 1°', 
    lu = u'39', 
    pampa = u'223', 
    basico_unc = 2741.75, 
    basico_nac = 2741.75, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Trab.Prácticos', 
    lu = u'40', 
    pampa = u'224', 
    basico_unc = 1749.7, 
    basico_nac = 1749.7, 
    horas = 21, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Vice Rector Escuela Artes', 
    lu = u'41', 
    pampa = u'225', 
    basico_unc = 2306.97, 
    basico_nac = 2306.97, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Bibliot.Ens. Superior', 
    lu = u'42', 
    pampa = u'226', 
    basico_unc = 2446.415, 
    basico_nac = 2446.415, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2403.16,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2403.16,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Preceptores', 
    lu = u'43', 
    pampa = u'227', 
    basico_unc = 2549.53, 
    basico_nac = 2549.53, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs. Cátedra Terciario', 
    lu = u'44', 
    pampa = u'228', 
    basico_unc = 211.55, 
    basico_nac = 211.55, 
    horas = 1, 
    tipo_horas = 'C',
	pago_por_hora = True
)
add_garantia_preuniv(
    cargo = c,
    valor = 233.42,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 233.42,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs. Cátedra Secundario', 
    lu = u'45', 
    pampa = u'229', 
    basico_unc = 169.24, 
    basico_nac = 169.24, 
    horas = 1, 
    tipo_horas = 'C',
	pago_por_hora = True
)
add_garantia_preuniv(
    cargo = c,
    valor = 186.58,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 186.58,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs. Cát. Inherentes a cargos', 
    lu = u'46', 
    pampa = u'230', 
    basico_unc = 2030.88, 
    basico_nac = 2030.88, 
    horas = 12, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Rector Educación Artística', 
    lu = u'49', 
    pampa = u'231', 
    basico_unc = 2198.41, 
    basico_nac = 2198.41, 
    horas = 12, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Profesor T.P (4)', 
    lu = u'50', 
    pampa = u'239', 
    basico_unc = 2092.085, 
    basico_nac = 2092.085, 
    horas = 12, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2238.98,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2238.98,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Equipo Tec.Pedagógico', 
    lu = u'51', 
    pampa = u'232', 
    basico_unc = 3618.6, 
    basico_nac = 3618.6, 
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Secretario 1° Categoría', 
    lu = u'52', 
    pampa = u'233',
    basico_unc = 4511.53,
    basico_nac = 4511.53,
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prosecretario Nivel Superior', 
    lu = u'53', 
    pampa = u'234',
    basico_unc = 1786.135,
    basico_nac = 1786.135,
    horas = 0, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'J.T.P T.C (Esc. Comercio)', 
    lu = u'55', 
    pampa = u'235',
    basico_unc = 2220.15,
    basico_nac = 2220.15,
    horas = 15, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2100,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2100,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. T.P (1)', 
    lu = u'57', 
    pampa = u'236',
    basico_unc = 5077.2,
    basico_nac = 5077.2,
    horas = 30, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5597.96,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5597.96,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. T.P (2)', 
    lu = u'58', 
    pampa = u'237',
    basico_unc = 4061.76,
    basico_nac = 4061.76,
    horas = 24, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 447796,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 4477.96,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Prof. T.P (3)', 
    lu = u'59', 
    pampa = u'238',
    basico_unc = 3046.32,
    basico_nac = 3046.32,
    horas = 18, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 3358.47,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 3358.47,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Auxiliar Docente', 
    lu = u'80', 
    pampa = u'241',
    basico_unc = 2856,
    basico_nac = 2856,
    horas = 25, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2718.04,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2718.04,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Vice Director 1° D.E', 
    lu = u'82', 
    pampa = u'302',
    basico_unc = 8568,
    basico_nac = 8568,
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de 1° D.E', 
    lu = u'83', 
    pampa = u'303',
    basico_unc = 3039.92,
    basico_nac = 3039.92,
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)

###############
c = add_cargo_preuniv(
    nombre = u'Sub Regente de 1° Cat. D.E', 
    lu = u'84', 
    pampa = u'304', 
    basico_unc = 5428.8, 
    basico_nac = 5428.8, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Sub Regente de 1° Categoría', 
    lu = u'85', 
    pampa = u'305', 
    basico_unc = 3293.473, 
    basico_nac = 3293.473, 
    horas = 27.3, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Secretario de 1° Categ.D.E', 
    lu = u'86', 
    pampa = u'306', 
    basico_unc = 6511.5, 
    basico_nac = 6511.5, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Dpto D.E', 
    lu = u'87', 
    pampa = u'307', 
    basico_unc = 2309.525, 
    basico_nac = 2309.525, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Gabinete Psicoped. D.E', 
    lu = u'88', 
    pampa = u'308', 
    basico_unc = 2329, 
    basico_nac = 2329, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Gabinetista D.E', 
    lu = u'89', 
    pampa = u'309', 
    basico_unc = 2264.08, 
    basico_nac = 2264.08, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Asesor Pedagógico', 
    lu = u'90', 
    pampa = u'310', 
    basico_unc = 1592.44, 
    basico_nac = 1592.44, 
    horas = 27.3, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Preceptores 1° D.E', 
    lu = u'91', 
    pampa = u'311', 
    basico_unc = 4935.15, 
    basico_nac = 4935.15, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Jefe Preceptores 1°', 
    lu = u'92', 
    pampa = u'312', 
    basico_unc = 2993.99, 
    basico_nac = 2993.99, 
    horas = 27.3, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2800,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayud. Gabinete Práctico D.E', 
    lu = u'93', 
    pampa = u'313', 
    basico_unc = 2196.98, 
    basico_nac = 2196.98, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayud. Gabinete Práctico', 
    lu = u'94', 
    pampa = u'314', 
    basico_unc = 2229.88, 
    basico_nac = 2229.88, 
    horas = 15, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2100,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2100,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Bibliotecario D.E', 
    lu = u'95', 
    pampa = u'315', 
    basico_unc = 2230.525, 
    basico_nac = 2230.525, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Preceptor D.E', 
    lu = u'96', 
    pampa = u'316', 
    basico_unc = 4589.17, 
    basico_nac = 4589.17, 
    horas = 45, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 5600,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Preceptor', 
    lu = u'97', 
    pampa = u'317', 
    basico_unc = 2572.45, 
    basico_nac = 2572.45, 
    horas = 27.3, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 2782.18,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 2782.18,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Horas Cátedra Secundario', 
    lu = u'98', 
    pampa = u'318', 
    basico_unc = 169.24, 
    basico_nac = 169.24, 
    horas = 0, 
    tipo_horas = 'C',
	pago_por_hora = True
)
add_garantia_preuniv(
    cargo = c,
    valor = 186.58,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 186.58,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Hs Cát. Inherentes a cargos', 
    lu = u'98', 
    pampa = u'319', 
    basico_unc = 2030.88, 
    basico_nac = 2030.88, 
    horas = 12, 
    tipo_horas = 'C',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 0,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Ayudante Gab. Psicoped.', 
    lu = u'99', 
    pampa = u'242', 
    basico_unc = 1896.14, 
    basico_nac = 1896.14, 
    horas = 10, 
    tipo_horas = 'R',
	pago_por_hora = False
)
add_garantia_preuniv(
    cargo = c,
    valor = 1400,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = 1400,
    mes = 'JUN',
    anio = '2012'
)

