import csv
import io
from datetime import datetime

import pytz
import unidecode
from catalogos_modular.models import Candado, Contenedor, CruceAvc
from django.apps import apps
from django.db.models import Q
from django.utils import timezone


def generate_csv_gafetes(queryset, user):
    header = [
        'Numero de gafete', 
        'Numero de gafete corto',
        'Folio cita',
        'Nombre de usuario', 
        'Extranjero',
        'RFC', 
        'CURP',
        'TAX ID', 
        'Pasaporte', 
        'Tipo de gafete', 
        'Fecha de vigencia',
        'Estado',
    ]
    stringIo = io.StringIO()
    writer = csv.writer(stringIo)
    writer.writerow(header)


    for value in queryset:
        if value.user.extranjero:
            extranjero = 'Si'
            rfc = ''
            curp = ''
            tax_id = value.user.tags_id
            pasaporte = value.user.pasaporte
        else:
            extranjero = 'No'
            rfc = value.user.rfc
            curp = value.user.curp
            tax_id = ''
            pasaporte = ''
        
        data = [
            unidecode.unidecode(value.numero_gafete),
            unidecode.unidecode(value.numero_gafete_corto),
            unidecode.unidecode(value.cita.folio),
            unidecode.unidecode(value.user.username), 
            unidecode.unidecode(extranjero), 
            unidecode.unidecode(rfc),
            unidecode.unidecode(curp),
            unidecode.unidecode(tax_id),
            unidecode.unidecode(pasaporte),
            unidecode.unidecode(str(value.tipo_gafete.tipo)),
            unidecode.unidecode(str(value.fecha_vigencia)),
            unidecode.unidecode(str(value.estado)),
        ]
        writer.writerow(data)

    stringIo.seek(0)

    buf = io.BytesIO()
    buf.write(stringIo.getvalue().encode())
    buf.seek(0)
    buf.name = 'Gafetes.csv'
    return buf