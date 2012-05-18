# -*- coding: utf-8 -*-

from django.db import models

from salary_calculator_app.validators import *


class Cargo(models.Model):
	lu 		= models.CharField(u'Código LU', max_length=2, unique=True, validators=[validate_isdigit])
	pampa 		= models.CharField(u'Código PAMPA', max_length=3, unique=True, validators=[validate_isdigit])
	tipo 		= models.CharField(u'Tipo de Cargo', max_length=50, unique=True)
	basico 		= models.FloatField(u'Sueldo Básico')
	garantia 	= models.FloatField(u'Garantía Salarial', blank=True, default=-1)

	def __unicode__(self):
		return unicode(self.lu) + " " + self.tipo


class CargoPreUniv(Cargo):
	horas = models.SmallIntegerField(u'Cantidad de Horas Cátedra')


class Antiguedad(models.Model):
	anio 		= models.SmallIntegerField(u'Años de Antiguedad', unique=True)
	porcentaje 	= models.FloatField(u'Porcentaje')

	def __unicode__(self):
		return unicode(self.anio) + " - " + unicode(self.porcentaje) + "%"


class Aumento(models.Model):
	fecha		= models.DateField(u'Fecha', unique=True)
	porcentaje 	= models.FloatField(u'Porcentaje')

	def __unicode__(self):
		return unicode(self.fecha) + " - " + unicode(self.porcentaje) + "%"


class Retencion(models.Model):
	codigo 	= models.CharField(u'Código', max_length=3, validators=[validate_isdigit])
	nombre  = models.CharField(u'Nombre', max_length=50)
	porcentage = models.FloatField(u'Porcentaje de Descuento')

	def __unicode__(self):
		return unicode(self.codigo) + " " + self.nombre


class Remuneracion(models.Model):
	codigo 	= models.CharField(u'Código', max_length=3, validators=[validate_isdigit])
	nombre = models.CharField(u'Nombre', max_length=50)
	porcentage = models.FloatField(u'Porcentaje de Incremento')

	def __unicode__(self):
		return unicode(self.codigo) + " " + self.nombre

#class GarantiaSalarial(models.Model):

