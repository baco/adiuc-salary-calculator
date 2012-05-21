# -*- coding: utf-8 -*-

from django.db import models

from salary_calculator_app.validators import *

APP_OPCS = (
    ('U', u'Cargos Universitarios'),
    ('P', u'Cargos Preuniversitarios')
)


class Cargo(models.Model):
    """Modelo abstracto que representa un Cargo, ya sea pre o universitario."""

    lu = models.CharField(u'Código LU', max_length=2, unique=True, validators=[validate_isdigit],
        help_text=u'El código L.U. del cargo que figura en la planilla de la UNC.')
    pampa = models.CharField(u'Código PAMPA', max_length=3, unique=True, validators=[validate_isdigit],
        help_text=u'El código PAMPA del cargo que figura en la planilla de la UNC.')
    nombre = models.CharField(u'Tipo de Cargo', max_length=50, unique=True,
        help_text=u'El nombre del cargo como figura en la planilla de la UNC. Ej: Profesor Titular D.E, Profesor Asociado D.S, etc')
    basico_unc = models.FloatField(u'Sueldo Básico UNC',
        help_text=u'El sueldo básico del cargo que figura en la planilla de la UNC. Los calculos de aumentos y salarios brutos/netos se calcularán tomando como base este valor')
    basico_nac = models.FloatField(u'Sueldo Básico Paritaria Nacional',
        help_text=u'El sueldo básico del cargo que figura en la planilla grande, es decir, la planilla de las paritarias nacionales. Se toma este valor para el cálculo de los aumentos')
    garantia_salarial = models.FloatField(u'Garantía Salarial', blank=True, null=True,
        help_text=u'La garantía salarial para este cargo. Si no se dispone de la información dejar el campo en blanco.')

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.lu) + " " + self.nombre


class CargoUniv(Cargo):
    """Cargo de docente Universitario."""

    TIPO_OPCS = (
        ('D.E', u'Dedicación Exclusiva'),
        ('D.S.E', u'Dedicación Semi Exclusiva'),
        ('D.S', u'Dedicación Simple')
    )
    tipo = models.CharField(max_length=5, choices=TIPO_OPCS,
        help_text=u'El tipo de dedicación para el cargo. Pueden ser dedicación exclusiva, semi-exclusiva o simple.')

    def __unicode__(self):
        return super(CargoUniv, self).__unicode__() + " " + self.tipo


class CargoPreUniv(Cargo):
    """Cargo de docente Preuniversitario."""

    horas = models.SmallIntegerField(u'Cantidad de Horas Cátedra',
        help_text=u'La cantidad de horas cátedra para el cargo como figuran en la planilla de la UNC. Ej: Al cargo "Vice Director de 1°" le corresponden 25 horas.')

    def __unicode__(self):
        return super(CargoPreUniv, self).__unicode__() + " " + unicode(self.horas) + "hs"


class AntiguedadUniv(models.Model):
    """Una entrada de la tabla de escala de antiguedad para los docentes Universitarios"""
    anio               = models.SmallIntegerField(u'Años de Antiguedad', unique=True,
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')
    porcentaje     = models.FloatField(u'Porcentaje',
        help_text=u'El porcentaje correspondiente al aumento para la cantidad de años de antigüedad seleccionado. Ej: Para 5 años corresponde un 30%.')

    def __unicode__(self):
        return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class AntiguedadPreUniv(models.Model):
    """Una entrada de la tabla de escala de antiguedad para los docentes Preuniversitarios"""

    anio               = models.SmallIntegerField(u'Años de Antiguedad', unique=True,
        help_text=u'La cantidad de años correspondiente a la antigüedad. Ej: 0, 1, 2, 5, 7, 9, 24, etc.')
    porcentaje     = models.FloatField(u'Porcentaje',
        help_text=u'El porcentaje correspondiente al aumento para la cantidad de años de antigüedad seleccionado. Ej: Para 2 años corresponde un 15%.')

    def __unicode__(self):
        return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class Aumento(models.Model):
    """Representa un aumento del salario basico."""

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
    YEARS_OPCS=tuple([(i, unicode(i)) for i in range(2000, 2020)])

    mes = models.CharField(u'Mes', max_length=3, choices=MONTHS_OPCS,
        help_text=u'El mes del aumento.')
    anio = models.CharField(u'Año', max_length=4, choices=YEARS_OPCS, validators=[validate_isdigit],
        help_text=u'El año del aumento.')
    porcentaje = models.FloatField(u'Porcentaje',
        help_text=u'El porcentage de aumento correspondiente. Ingresar valores entre 0 y 100. Por ejemplo, para Marzo de 2012 hay un aumento del 6%')

    def __unicode__(self):
        return self.mes + " " + self.anio + " - " + unicode(self.porcentaje) + "%"


class RemuneracionRetencion(models.Model):
    """Modelo abstracto que junta los atributos en comun que tiene una retencion y una remuneracion"""

    codigo     = models.CharField(u'Código', max_length=3, validators=[validate_isdigit])
    nombre  = models.CharField(u'Nombre', max_length=50)
    aplicacion = models.CharField(u'Aplica a', max_length=1, choices=APP_OPCS)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.codigo + " " + self.nombre


class RetencionPorcentual(RemuneracionRetencion):
    porcentage = models.FloatField(u'Porcentaje de Descuento')

    def __unicode__(self):
        return super(RetencionPorcentual, self).__unicode__() + " " + unicode(self.porcentage ) + "%"


class RetencionFija(RemuneracionRetencion):
    valor = models.FloatField(u'Valor de Descuento')

    def __unicode__(self):
        return super(RetencionFija, self).__unicode__() + u" $" + unicode(self.valor)


class RemuneracionPorcentual(RemuneracionRetencion):
    porcentage = models.FloatField(u'Porcentaje de Descuento')

    def __unicode__(self):
        return super(RemuneracionPorcentual, self).__unicode__() + " " + unicode(self.porcentage) + "%"


class RemuneracionFija(RemuneracionRetencion):
    valor = models.FloatField(u'Valor de Descuento')

    def __unicode__(self):
        return super(RetencionPorcentual, self).__unicode__() + u" $" + unicode(self.valor)

