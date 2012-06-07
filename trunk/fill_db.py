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


#=============================================#
#						CARGOS UNIVERSITARIOS												  #
#=============================================#
#c = Cargo(lu='5', pampa='101', tipo='Profesor Titular D.E', basico=6831.76)
#c.save()
#c = Cargo(lu='13', pampa='102', tipo='Profesor Titular D.S.E', basico=3415.88)
#c.save()
#c = Cargo(lu='27', pampa='103', tipo='Profesor Titular D.S', basico=1707.94)
#c.save()
#c = Cargo(lu='6', pampa='105', tipo='Profesor Asociado D.E', basico=6146.54)
#c.save()
#c = Cargo(lu='8', pampa='106', tipo='Profesor Asociado D.S.E', basico=3073.27)
#c.save()

# TODO: Complete with the rest of the teaching positions

#=============================================#
#						CARGOS PREUNIVERSITARIOS											   #
#=============================================#
def add_cargo_preuniv(nombre, lu, pampa, basico_unc, basico_nac, horas, tipo_horas):
    t = TipoCargo(nombre=nombre)
    t.save()
    c = CargoPreUniv(lu=lu, pampa=pampa, tipo=t, basico_unc=basico_unc, basico_nac=basico_nac, horas=horas, tipo_horas=tipo_horas)
    c.save()
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
    g = GarantiaSalarial(valor=valor, mes=mes, anio=anio)
    g.save()
    cargo.garantia_salarial.add(g)


# Base: Copiar y pegar este
###############
c = add_cargo_preuniv(
    nombre = u'', 
    lu = u'', 
    pampa = u'', 
    basico_unc = , 
    basico_nac = , 
    horas = , 
    tipo_horas = ''
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'JUN',
    anio = '2012'
)


pdb.set_trace()

c = add_cargo_preuniv(
    nombre = u'Vice Director de 1°', 
    lu = u'1', 
    pampa = u'201', 
    basico_unc = 5079.6, 
    basico_nac = 5079.6, 
    horas = 25, 
    tipo_horas = 'R'
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
    tipo_horas = 'R'
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
    tipo_horas = 'R'
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
    tipo_horas = 'C'
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
    tipo_horas = 'C'
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
    tipo_horas = 'R'
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
    tipo_horas = 'C'
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
    tipo_horas = 'R'
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
    tipo_horas = 'R'
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
    tipo_horas = 'R'
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
    tipo_horas = 'R'
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
    tipo_horas = 'R'
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
    nombre = u'Director de 3o Categoría', 
    lu = u'21', 
    pampa = u'213', 
    basico_unc = 1994.97, 
    basico_nac = 1994.97, 
    horas = 35, 
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Regente de 1o Esc.Superior', 
    lu = u'24', 
    pampa = u'215', 
    basico_unc = 2219.31, 
    basico_nac = 2219.31, 
    horas = 35, 
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'JUN',
    anio = '2012'
)
###############
c = add_cargo_preuniv(
    nombre = u'Secret. de 1o Categoría', 
    lu = u'25', 
    pampa = u'216', 
    basico_unc = 1786.14, 
    basico_nac = 1786.14, 
    horas = 35, 
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'JUN',1749.7
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,Vice Rector Escuela Artes
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
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
    tipo_horas = 'R'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'MAR',
    anio = '2012'
)
add_garantia_preuniv(
    cargo = c,
    valor = ,
    mes = 'JUN',
    anio = '2012'
)
