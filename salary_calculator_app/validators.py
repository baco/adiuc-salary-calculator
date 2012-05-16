# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError

def validate_isdigit(string):
	"""string es valido si no es vacio y si todos sus caracteres son digitos
	(0..9).
	Pre: string es una cadena de caracteres de python"""

	if not string.isdigit():
		raise ValidationError(u'Debe ingresar caracteres numéricos: "0", "1", "2", ... , "7", "8", "9".')
