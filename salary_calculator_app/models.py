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


class GarantiaSalarialPreUniversitaria(models.Model):
    """ garantía salarial para cargos preuniversitarios """
    
    cargo = models.ForeignKey('CargoPreUniversitario',
        help_text=u'El cargo docente sobre el que se aplica esta garantía.')
    
    valor = models.FloatField(u'Monto minimo', validators=[validate_isgezero],
        help_text=u'Monto mínimo, igualado éste no se aplica la garantía.')

    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta garantía comienza a tener vigencia.')

    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta garantía deja de ser vigente.')

class GarantiaSalarialUniversitaria(models.Model):
    """Representa el valor minimo que un Cargo puede cobrar."""

    cargo = models.ForeignKey('CargoUniversitario',
        help_text=u'El cargo docente sobre el que se aplica esta garantía.')

    valor_minimo = models.FloatField(u'Monto minimo', validators=[validate_isgezero],
        help_text=u'Monto mínimo, igualado éste no se aplica la garantía.')

    valor_st = models.FloatField(u'Monto de la garantía', validators=[validate_isgezero],
        help_text=u'El monto de esta garantía sin título adicional.')
    valor_doctorado = models.FloatField(u'Monto de la garantía', validators=[validate_isgezero],
        help_text=u'El monto de esta garantía con título de doctorado.')
    valor_master = models.FloatField(u'Monto de la garantía', validators=[validate_isgezero],
        help_text=u'El monto de esta garantía con título de master.')
    
    antiguedad_min = models.IntegerField(u'Antiguedad mínima',
        help_text=u'A partir de esta antiguedad corresponde el monto asociado a la garantía.' )
    
    antiguedad_max = models.IntegerField(u'Antiguedad máxima',
        help_text=u'Hasta esta antiguedad (inclusive) corresponde el monto asociado a la garantía.' )
    
    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta garantía comienza a tener vigencia.')

    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta garantía deja de ser vigente.')    

    class Meta:
        ordering = ['cargo', 'valor_minimo']

    def __unicode__(self):
        return unicode(self.cargo) + " $" + unicode(self.valor) + " [" + unicode(self.vigencia_desde) + " / " + unicode(self.vigencia_hasta) + "]"


class Cargo(models.Model):
    """Modelo abstracto que representa un Cargo, ya sea pre o universitario."""

    lu = models.CharField(u'Código LU', max_length=2, validators=[validate_isdigit],
        help_text=u'El código L.U. del cargo que figura en la planilla de la UNC.')
    pampa = models.CharField(u'Código PAMPA', max_length=3, unique=True, validators=[validate_isdigit],
        help_text=u'El código PAMPA del cargo que figura en la planilla de la UNC.')
    denominacion = models.ForeignKey('DenominacionCargo',
        help_text=u'El nombre del cargo asociado.')

    #rem_fijas = models.ManyToManyField('RemuneracionFija', blank=True)
    #rem_porcentuales = models.ManyToManyField('RemuneracionPorcentual', blank=True)
    #ret_fijas = models.ManyToManyField('RetencionFija', blank=True)
    #ret_porcentuales = models.ManyToManyField('RetencionPorcentual', blank=True)

    class Meta:
        ordering = ['denominacion']

    def __unicode__(self):
        #return self.lu + " - " + unicode(self.denominacion)
        return unicode(self.denominacion)


class DenominacionCargo(models.Model):
    """El nombre de un cargo docente. Ej: Profesor Adjunto, Ayudante Alumno, etc"""

    nombre = models.CharField(u'Denominacion del Cargo', max_length=50, unique=True,
        help_text=u'El nombre de un cargo docente. Ej: Profesor Titular, Profesor Asociado, etc')
    
    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class CargoUniversitario(Cargo):
    """Cargo de docente Universitario."""

    DEDICACION_OPCS = (
        ('D.E', u'Dedicación Exclusiva'),
        ('D.S.E', u'Dedicación Semi Exclusiva'),
        ('D.S', u'Dedicación Simple')
    )
    dedicacion = models.CharField(u'Dedicación', max_length=5, choices=DEDICACION_OPCS,
        help_text=u'El tipo de dedicación para el cargo. Pueden ser dedicación exclusiva, semi-exclusiva o simple.')
    #adic2003 = models.FloatField(u'Adic. 8% RHCS 153/03', blank=True, null=True,	
    #help_text=u'Es el adicional del 8% del salario básico del año 2003 que le corresponde a este cargo.')

    def __unicode__(self):
        return super(CargoUniversitario, self).__unicode__() + " - " + self.dedicacion


class CargoPreUniversitario(Cargo):
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
            return super(CargoPreUniversitario, self).__unicode__()
        return super(CargoPreUniversitario, self).__unicode__() + " - " + unicode(self.horas) + "hs"


class RemuneracionRetencion(models.Model):
    """Modelo abstracto que junta los atributos en comun que tiene una retencion y una remuneracion."""

    MODO_OPCS = (
        ('P', u'Se aplica a la persona (solo una vez).'),
        ('C', u'Se aplica por cargo (una vez por cada cargo).'),
    )

    # Tuplas de opciones.
    APP_OPCS = (
        ('U', u'Cargos Universitarios'),
        ('P', u'Cargos Preuniversitarios'),
        ('T', u'Todos los cargos')
    )

    codigo = models.CharField(u'Código', max_length=5,
        help_text=u'El código de remuneración/retención tal cual figura en la lista de la web de ADIUC.')
    nombre  = models.CharField(u'Nombre', max_length=50,
        help_text=u'El nombre de la remuneración/retención tal cual figura en la lista de la web de ADIUC.')
    aplicacion = models.CharField(u'Aplica a', max_length=1, choices=APP_OPCS,
        help_text=u'A qué tipo de cargo aplica esta remuneración/retención.')
    modo = models.CharField(u'Modo', max_length=1,choices=MODO_OPCS)

    class Meta:
        ordering = ['codigo', 'nombre', 'aplicacion']

    def __unicode__(self):
        return self.codigo + u" " + self.nombre


class RetencionPorcentual(models.Model):
    """Una retencion que especifica el porcentaje del descuento que debe realizarse."""

    retencion = models.ForeignKey('RemuneracionRetencion',
        help_text = u'La retención relacionada con esta retención porcentual.')
    porcentaje = models.FloatField(u'Porcentaje de Descuento', validators=[validate_isgezero],
        help_text=u'El porcentaje del descuento. Ingresar un valor positivo.')
    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta retención porcentual comienza a tener vigencia.')
    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta retención porcentual deja de ser vigente.')

    class Meta:
        ordering = ['retencion', 'porcentaje']

    def __unicode__(self):
        return unicode(self.retencion) + u" " + unicode(self.porcentaje) + u"%"


class RetencionDaspu(models.Model):
    """ Representa las retenciones para DASPU """
    
    #No usa retencion fija, porque necesita dos porcentajes.    
    retencion = models.ForeignKey('RemuneracionRetencion',
        help_text = u'La retención relacionada con esta retención porcentual.')

    porcentaje_personal = models.FloatField(u'Porcentaje de descuento de contribución personal',
        help_text=u'Porcentaje de retención de aporte personal.')
        
    porcentaje_patronal = models.FloatField(u'Porcentaje de descuento de aporte patronal.',
        help_text=u'Porcentaje de retención de contribución patronal.')
    
    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta retención comienza a tener vigencia.')

    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta retención deja de ser vigente.') 

    def __unicode__(self):
            return u"Retención DASPU: [" + unicode(self.porcentaje_patronal) + u"% - " + unicode(self.porcentaje_personal) + u"%] - [" + unicode(self.vigencia_desde) + u" / " + unicode(self.vigencia_hasta) + u"]"


class RetencionFija(models.Model):
    """Una retencion que especifica un descuento fijo que debe realizarse."""

    retencion = models.ForeignKey('RemuneracionRetencion',
        help_text = u'La retención relacionada con esta retención porcentual.')
    valor = models.FloatField(u'Valor de Descuento', validators=[validate_isgezero],
        help_text=u'El valor fijo que debe descontarse.')
    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta retención porcentual comienza a tener vigencia.')
    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta retención porcentual deja de ser vigente.')

    class Meta:
        ordering = ['retencion', 'valor']

    def __unicode__(self):
        return unicode(self.retencion) + u" $" + unicode(self.valor)

class FondoSolidario(RetencionFija):
    concepto = models.CharField(u'Concepto', max_length='50')
    
class RemuneracionPorcentual(models.Model):
    """Una remuneracion que especifica el porcentaje de aumento que debe realizarse."""

    remuneracion = models.ForeignKey('RemuneracionRetencion',
        help_text = u'La retención relacionada con esta remuneración porcentual.')
    porcentaje = models.FloatField(u'Porcentaje de Aumento', validators=[validate_isgezero],
        help_text=u'El porcentaje del aumento. Ingresar un valor positivo.')
    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta remuneración porcentual comienza a tener vigencia.')
    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta remuneración porcentual deja de ser vigente.')

    class Meta:
        ordering = ['remuneracion', 'porcentaje']

    def __unicode__(self):
        return unicode(self.porcentaje) + u"% - " + unicode(self.remuneracion)


class RemuneracionFija(models.Model):
    """Una remuneracion que especifica un aumento fijo sobre el salario basico."""

    remuneracion = models.ForeignKey('RemuneracionRetencion',
        help_text = u'La retención relacionada con esta remuneración fija.')
    valor = models.FloatField(u'Valor del Aumento', validators=[validate_isgezero],
        help_text=u'El valor fijo que se sumará al salario básico.')
    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta remuneración fija comienza a tener vigencia.')
    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta remuneración fija deja de ser vigente.')

    class Meta:
        ordering = ['remuneracion', 'valor']

    def __unicode__(self):
        return u"$" + unicode(self.valor) + " - " + unicode(self.remuneracion)

#class ConceptoAsigFamiliar(models.Model):
#    concepto = models.CharField(u'Concepto de asignación', max_length='50', help_text=u'Concepto de asignación familiar.')
#
#    class Meta:
#        ordering = ['concepto']
#
#    def __unicode__(self):
#        return unicode(self.concepto)
        
#class CategoriaAsigFamiliar(models.Model):
#    valor_min = models.FloatField(u'Valor mínimo:',help_text=u'Valor mínimo de categoría.')
#    valor_max = models.FloatField(u'Valor máximo:', help_text=u'Valor máximo de categoría.')
#
#    def clean(self):
#        from django.core.exceptions import ValidationError
#        if self.valor_min > valor_max:
#            raise ValidationError('El valor mínimo debe ser menor al valor máximo.')
#    class Meta:
#        ordering = ['valor_min','valor_max']

#    def __unicode__(self):
#       return unicode(self.valor_min) + u" - " + unicode(self.valor_max)


class AsignacionFamiliar(models.Model):
    """Representa uan asignación familiar."""
# Antes heredaba de remuneracionFIja, pero es necesario poder dejar en blank algunos valores.
#    concepto = models.ForeignKey('ConceptoAsigFamiliar',help_text=u'Concepto de la asignación.')
#    categoria = models.OneToOneField('CategoriaAsigFamiliar',help_text=u'Categoría de la asignación.')

    remuneracion = models.ForeignKey('RemuneracionRetencion',
        help_text = u'La remuneración asociada a esta asignación.')

    concepto = models.CharField(u'Concepto de asignación', max_length='50', help_text=u'Concepto de la asignación.')

    valor = models.FloatField(u'Valor del Aumento', validators=[validate_isgezero],
        help_text=u'El valor fijo que se sumará al salario básico.')

    valor_min = models.FloatField(u'Valor mínimo:',
        help_text=u'Valor mínimo de categoría.')

    valor_max = models.FloatField(u'Valor máximo:',
        help_text=u'Valor máximo de categoría.')

    vigencia_desde = models.DateField(u'Vigente desde',
        help_text=u'Fecha a partir de la cual esta remuneración fija comienza a tener vigencia.')

    vigencia_hasta = models.DateField(u'Vigente hasta',
        help_text=u'Fecha a partir de la cual esta remuneración fija deja de ser vigente.')


    def clean(self):
        from django.core.exceptions import ValidationError
        if self.valor_min > self.valor_max:
            raise ValidationError('El valor mínimo debe ser menor al valor máximo.')
    
    class Meta:
        ordering = ['concepto']

    def __unicode__(self):
        return unicode(self.concepto) + u" - [ " + unicode(self.valor_min) +u" / " + unicode(self.valor_max) + u" ]"


class SalarioBasico(RemuneracionFija):
    """Representavalor_min = models.FloatField(u'Valor mínimo:',help_text=u'Valor mínimo de categoría.')
    valor_max = models.FloatField(u'Valor máximo:', help_text=u'Valor máximo de categoría.') un valor de un salario basico relacionado a un cargo."""

    cargo = models.ForeignKey('Cargo',
        help_text=u'El cargo docente sobre el que se aplica este salario.')

    class Meta:
        ordering = ['cargo', 'valor']

    def __unicode__(self):
        return unicode(self.cargo) + u" - $" + unicode(self.valor) + u" - [" + unicode(self.vigencia_desde) + u" / " + unicode(self.vigencia_hasta) + u"]"


class AntiguedadUniversitaria(RemuneracionPorcentual):
    """Una entrada de la tabla de escala de antiguedad para los docentes Universitarios"""

    anio = models.SmallIntegerField(u'Años de Antigüedad', validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')

    class Meta:
        ordering = ['anio']

    def __unicode__(self):
        return unicode(self.anio) + u" años - " + unicode(self.porcentaje) + u"% - [" + unicode(self.vigencia_desde) + u" / " + unicode(self.vigencia_hasta) + u"]"


class AntiguedadPreUniversitaria(RemuneracionPorcentual):
    """Una entrada de la tabla de escala de antiguedad para los docentes Preuniversitarios"""

    anio = models.SmallIntegerField(u'Años de Antigüedad', validators=[validate_isgezero],
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')

    class Meta:
        ordering = ['anio']

    def __unicode__(self):
        return unicode(self.anio) + u" años - " + unicode(self.porcentaje) + u"% - [" + unicode(self.vigencia_desde) + u" / " + unicode(self.vigencia_hasta) + u"]"

