import os
import re

from django.db.models import Q

PRUEBAS = os.environ.get('PRUEBAS') == 'True'


def validate_characters(text):
    # Regex for validating characters, spaces, numbers and accents
    regex = re.compile(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$')
    return regex.match(text)
        
def validate_alphanumeric(text):
    # Regex for validating characters, spaces, numbers and accents
    regex = re.compile(r'^[a-zA-Z0-9]+$')
    return regex.match(text)

def is_anam_mail(email):
    if PRUEBAS:
        return True
    if email is None:
        return False
    if re.fullmatch(r'^[a-zA-Z0-9ñÑ_.]+@anam.gob.mx$', email, re.IGNORECASE):
        return True	
    return False

def is_valid_mail(email):
	if email is None:
		return False
	# check regex if email is valid
	if re.fullmatch(r'^[a-zA-Z0-9_.ñÑ]+@[a-zA-Z0-9.]+$', email, re.IGNORECASE):
		return True
	return False

def tiene_documentos(user):
    return user.destinatario.filter(~Q(documento__estado_doc__estado_doc='Cierre verificado')).exists()