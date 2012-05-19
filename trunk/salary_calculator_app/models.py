# -*- coding: utf-8 -*-

from django.db import models

from salary_calculator_app.validators import *

APP_OPCS = (
    ('U', u'Cargos Universitarios'),
    ('P', u'Cargos Preuniversitarios')
)


class Cargo(models.Model):
    lu = models.CharField(u'Código LU', max_length=2, unique=True, validators=[validate_isdigit])
    pampa = models.CharField(u'Código PAMPA', max_length=3, unique=True, validators=[validate_isdigit])
    nombre = models.CharField(u'Tipo de Cargo', max_length=50, unique=True)
    basico_unc = models.FloatField(u'Sueldo Básico UNC')
    basico_nac = models.FloatField(u'Sueldo Básico Paritaria Nacional')
    garantia_salarial = models.FloatField(u'Garantía Salarial', blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.lu) + " " + self.nombre


class CargoUniv(Cargo):
    TIPO_OPCS = (
        ('D.E', u'Dedicación Exclusiva'),
        ('D.S.E', u'Dedicación Semi Exclusiva'),
        ('D.S', u'Dedicación Simple')
    )
    tipo = models.CharField(max_length=5, choices=TIPO_OPCS)

    def __unicode__(self):
        return super(CargoUniv, self).__unicode__() + " " + tipo


class CargoPreUniv(Cargo):
    horas = models.SmallIntegerField(u'Cantidad de Horas Cátedra')

    def __unicode__(self):
        return super(CargoPreUniv, self).__unicode__() + " " + unicode(horas) + "hs"


class AntiguedadUniv(models.Model):
    anio               = models.SmallIntegerField(u'Años de Antiguedad', unique=True)
    porcentaje     = models.FloatField(u'Porcentaje')

    def __unicode__(self):
        return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class AntiguedadPreUniv(models.Model):
    anio               = models.SmallIntegerField(u'Años de Antiguedad', unique=True)
    porcentaje     = models.FloatField(u'Porcentaje')

    def __unicode__(self):
        return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class Aumento(models.Model):
    fecha = models.DateField(u'Fecha', unique=True)
    porcentaje = models.FloatField(u'Porcentaje')

    def __unicode__(self):
        return unicode(self.fecha) + " - " + unicode(self.porcentaje) + "%"


class RemuneracionRetencion(models.Model):
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
        return super(RetencionPorcentual, self).__unicode__() + " " + unicode(porcentage ) + "%"


class RetencionFija(RemuneracionRetencion):
    valor = models.FloatField(u'Valor de Descuento')

    def __unicode__(self):
        return super(RetencionFija, self).__unicode__() + " " + unicode(porcentage)


class RemuneracionPorcentual(RemuneracionRetencion):
    porcentage = models.FloatField(u'Porcentaje de Descuento')

    def __unicode__(self):
        return super(RemuneracionPorcentual, self).__unicode__() + " " + unicode(porcentage) + "%"


class RemuneracionFija(RemuneracionRetencion):
    valor = models.FloatField(u'Valor de Descuento')

    def __unicode__(self):
        return super(RetencionPorcentual, self).__unicode__() + " " + unicode(porcentage )

