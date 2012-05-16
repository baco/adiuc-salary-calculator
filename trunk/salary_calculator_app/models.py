# -*- coding: utf-8 -*-

from django.db import models

from validators import *

class Cargo(models.Model):
	lu 				= models.CharField(u'Código LU', max_length=2, unique=True, validators=[validate_isdigit])
	pampa 		= models.CharField(u'Código PAMPA', max_length=3, unique=True, validators=[validate_isdigit])
	tipo 			= models.CharField(u'Tipo de Cargo', max_length=50, unique=True)
	basico 		= models.FloatField(u'Sueldo Básico')
	garantia 	= models.FloatField(u'Garantía Salarial')

	def __unicode__(self):
		return self.lu + " " + self.tipo

class Antiguedad(models.Model):
	anio 				= models.SmallIntegerField(u'Años de Antiguedad', unique=True)
	porcentaje 	= models.FloatField()
