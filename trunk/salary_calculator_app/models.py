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

from django.db import models

from salary_calculator_app.validators import *

# Tuplas de opciones.
APP_OPCS = (
    ('U', u'Cargos Universitarios'),
    ('P', u'Cargos Preuniversitarios'),
    ('T', u'Todos los cargos')
)
MONTHS_OPCS=(
        ('ENE', u'Enero'),
        ('FEB', u'Febrero'),
        ('MAR', u'Marzo'),
        ('ABR', u'Abril'),
        ('MAY', u'Mayo'),
        ('JUN', u'Junio'),
        ('JUL', u'Julio'),
        ('AGO', u'Agosto'),
        ('SEP', u'Septiembre'),
        ('OCT', u'Octubre'),
        ('NOV', u'Noviembre'),
        ('DIC', u'Diciembre'),
)
YEARS_OPCS=tuple([(unicode(i), unicode(i)) for i in range(2000, 2020)])


class Cargo(models.Model):
    """Modelo abstracto que representa un Cargo, ya sea pre o universitario."""

    lu = models.CharField(u'Código LU', max_length=2, validators=[validate_isdigit],
        help_text=u'El código L.U. del cargo que figura en la planilla de la UNC.')
    pampa = models.CharField(u'Código PAMPA', max_length=3, unique=True, validators=[validate_isdigit],
        help_text=u'El código PAMPA del cargo que figura en la planilla de la UNC.')
    tipo = models.ForeignKey('TipoCargo',
        help_text=u'El nombre o tipo de cargo asociado.')
    basico_unc = models.FloatField(u'Sueldo Básico UNC', validators=[validate_isgezero],
        help_text=u'El sueldo básico del cargo que figura en la planilla de la UNC. Los cálculos de aumentos y salarios brutos/netos se calcularán tomando como base este valor.')
    basico_nac = models.FloatField(u'Sueldo Básico Paritaria Nacional', validators=[validate_isgezero],
        help_text=u'El sueldo básico del cargo que figura en la planilla grande, es decir, la planilla de las paritarias nacionales. Se toma este valor para el cálculo de los aumentos')
    garantia_salarial = models.ManyToManyField('GarantiaSalarial', blank=True, null=True,
        help_text=u'La garantía salarial asociada a este cargo. Es el monto mínimo que una persona con el cargo puede cobrar.')
    rem_fijas = models.ManyToManyField('RemuneracionFija',blank=True)
    rem_porcentuales = models.ManyToManyField('RemuneracionPorcentual',blank=True )
    ret_fijas = models.ManyToManyField('RetencionFija',blank=True )
    ret_porcentuales = models.ManyToManyField('RetencionPorcentual',blank=True )

    class Meta:
        abstract = True
        ordering = ['tipo']

    def __unicode__(self):
        #return self.lu + " - " + unicode(self.tipo)
        return unicode(self.tipo)


class TipoCargo(models.Model):
    """El nombre o tipo de cargo. Ej: Profesor Adjunto, Ayudante Alumno, etc"""

    nombre = models.CharField(u'Tipo de Cargo', max_length=50,
        help_text=u'El nombre de un tipo de cargo como figura en la planilla de la UNC. Ej: Profesor Titular, Profesor Asociado, etc')
    
    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class GarantiaSalarial(models.Model):
    """Representa el valor minimo que un Cargo puede cobrar."""

    valor = models.FloatField(u'Valor de la garantía', validators=[validate_isgezero],
        help_text=u'La garantía salarial para este cargo.')
    mes = models.CharField(u'Mes', max_length=3, choices=MONTHS_OPCS,
        help_text=u'El mes en que se definió la garantía.')
    anio = models.CharField(u'Año', max_length=4, choices=YEARS_OPCS, validators=[validate_isdigit],
        help_text=u'El año en que se definió la garantía.')

    class Meta:
        ordering = ['anio', 'mes', 'valor']

    def __unicode__(self):
        return "$" + unicode(self.valor) + " - " + self.mes + " " + self.anio


class CargoUniv(Cargo):
    """Cargo de docente Universitario."""

    DEDICACION_OPCS = (
        ('D.E', u'Dedicación Exclusiva'),
        ('D.S.E', u'Dedicación Semi Exclusiva'),
        ('D.S', u'Dedicación Simple')
    )
    dedicacion = models.CharField(u'Dedicación', max_length=5, choices=DEDICACION_OPCS,
        help_text=u'El tipo de dedicación para el cargo. Pueden ser dedicación exclusiva, semi-exclusiva o simple.')
    adic2003 = models.FloatField(u'Adic. 8% RHCS 153/03', blank=True, null=True,	
        help_text=u'Es el adicional del 8% del salario básico del año 2003 que le corresponde a este cargo.')

    def __unicode__(self):
        return super(CargoUniv, self).__unicode__() + " - " + self.dedicacion


class CargoPreUniv(Cargo):
    """Cargo de docente Preuniversitario."""

    TIPOHORAS_OPCS = (
        ('C', u'Cátedra'),
        ('R', u'Relog')
    )
    horas = models.FloatField(u'Cantidad de Horas Cátedra', validators=[validate_isgezero],
        help_text=u'La cantidad de horas para el cargo como figuran en la planilla de la UNC. Ej: Al cargo "Vice Director de 1°" le corresponden 25 horas.')
    tipo_horas = models.CharField(u'Tipo de Horas', max_length=1, choices=TIPOHORAS_OPCS,
        help_text=u'El tipo de horas del cargo.')
    pago_por_hora=models.BooleanField(u'Pago por hora?', 
        help_text=u'Poner "Sí" si este cargo se paga por cantidad de horas. Poner "No" en caso contrario.')

    def __unicode__(self):
        if self.pago_por_hora or self.horas <= 0.:
            return super(CargoPreUniv, self).__unicode__()
        return super(CargoPreUniv, self).__unicode__() + " - " + unicode(self.horas) + "hs"


class AntiguedadUniv(models.Model):
    """Una entrada de la tabla de escala de antiguedad para los docentes Universitarios"""
    anio               = models.SmallIntegerField(u'Años de Antiguedad', unique=True, validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')
    porcentaje     = models.FloatField(u'Porcentaje', validators=[validate_isgezero],
        help_text=u'El porcentaje correspondiente al aumento para la cantidad de años de antigüedad seleccionado. Ej: Para 5 años corresponde un 30%.')

    class Meta:
        ordering = ['anio']

    def __unicode__(self):
        return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class AntiguedadPreUniv(models.Model):
    """Una entrada de la tabla de escala de antiguedad para los docentes Preuniversitarios"""

    anio = models.SmallIntegerField(u'Años de Antiguedad', unique=True, validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')
    porcentaje = models.FloatField(u'Porcentaje', validators=[validate_isgezero],
        help_text=u'El porcentaje correspondiente al aumento para la cantidad de años de antigüedad seleccionado. Ej: Para 2 años corresponde un 15%.')

    class Meta:
        ordering = ['anio']

    def __unicode__(self):
        return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class Aumento(models.Model):
    """Representa un aumento del salario basico."""

    mes = models.CharField(u'Mes', max_length=3, choices=MONTHS_OPCS,
        help_text=u'El mes del aumento.')
    anio = models.CharField(u'Año', max_length=4, choices=YEARS_OPCS, validators=[validate_isdigit],
        help_text=u'El año del aumento.')
    porcentaje = models.FloatField(u'Porcentaje', validators=[validate_isgezero],
        help_text=u'El porcentaje de aumento correspondiente. Ingresar valores entre 0 y 100. Por ejemplo, para Marzo de 2012 hay un aumento del 6%')

    class Meta:
        ordering = ['anio', 'mes', 'porcentaje']

    def __unicode__(self):
        return self.mes + " " + self.anio + " - " + unicode(self.porcentaje) + "%"


class RemuneracionRetencion(models.Model):
    """Modelo abstracto que junta los atributos en comun que tiene una retencion y una remuneracion."""

    MODO_OPCS = (
        ('P', u'Se aplica a la persona (solo una vez).'),
        ('C', u'Se aplica por cargo (una vez por cada cargo).'),
    )

    codigo = models.CharField(u'Código', max_length=3, validators=[validate_isdigit],
        help_text=u'El código de remuneración/retención tal cual figura en la lista de la web de ADIUC.')
    nombre  = models.CharField(u'Nombre', max_length=50,
        help_text=u'El nombre de la remuneración/retención tal cual figura en la lista de la web de ADIUC.')
    aplicacion = models.CharField(u'Aplica a', max_length=1, choices=APP_OPCS,
        help_text=u'A qué tipo de cargo aplica esta remuneración/retención.')
    modo = models.CharField(u'Modo', max_length=1,choices=MODO_OPCS)

    class Meta:
        abstract = True
        ordering = ['codigo', 'nombre', 'aplicacion']

    def __unicode__(self):
        return self.codigo + " " + self.nombre


class RetencionPorcentual(RemuneracionRetencion):
    """Una retencion que especifica el porcentaje del descuento que debe realizarse."""

    porcentaje = models.FloatField(u'Porcentaje de Descuento', validators=[validate_isgezero],
        help_text=u'El porcentaje del descuento. Ingresar un valor positivo.')

    def __unicode__(self):
        return super(RetencionPorcentual, self).__unicode__() + " " + unicode(self.porcentaje ) + "%"


class RetencionFija(RemuneracionRetencion):
    """Una retencion que especifica un descuento fijo que debe realizarse."""

    valor = models.FloatField(u'Valor de Descuento', validators=[validate_isgezero],
        help_text=u'El valor fijo que debe descontarse.')

    def __unicode__(self):
        return super(RetencionFija, self).__unicode__() + u" $" + unicode(self.valor)


class RemuneracionPorcentual(RemuneracionRetencion):
    """Una remuneracion que especifica el porcentaje de aumento que debe realizarse."""
    porcentaje = models.FloatField(u'Porcentaje de Aumento', validators=[validate_isgezero],
        help_text=u'El porcentaje del aumento. Ingresar un valor positivo.')

    def __unicode__(self):
        return super(RemuneracionPorcentual, self).__unicode__() + " " + unicode(self.porcentaje) + "%"


class RemuneracionFija(RemuneracionRetencion):
    """Una remuneracion que especifica un aumento fijo sobre el salario basico."""

    valor = models.FloatField(u'Valor del Aumento', validators=[validate_isgezero],
        help_text=u'El valor fijo que se sumará al salario básico.')

    def __unicode__(self):
        return super(RemuneracionFija, self).__unicode__() + u" $" + unicode(self.valor)

