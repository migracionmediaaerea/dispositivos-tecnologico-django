import csv
from datetime import datetime, timedelta

from catalogos_modular.models import TrackReporte
from catalogos_modular.utils import (generate_csv_and_send_email,
                                     get_querset_by_model, is_valid_params)
from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django_q.tasks import async_task

from apps.dispositivos.views import IndexTagView as DispositivosIndex

from .utils import (ALLOWED_MODELS, ALLOWED_MODELS_DELETED, CUSTOM_CSV_CONTEXT,
                    PERMISOS_CSV, PERMISOS_CUSTOM_CSV)

meses = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre',
}
 
TIPO_REPORTES = {
    'Semaforo': TrackReporte.TipoReporte.AVC_SEMAFORO,
    'RojoAvc': TrackReporte.TipoReporte.AVC_ROJO,
    'ModuladoAvc': TrackReporte.TipoReporte.AVC_MODULADO,
    'TotalidadAvisoCruce': TrackReporte.TipoReporte.AVC_TOTALIDAD,
    'Pedimento': TrackReporte.TipoReporte.PEDIMENTO,
    'AvisoCruce': TrackReporte.TipoReporte.AVC_TOTALIDAD,
}

class GenerateCsv(LoginRequiredMixin, View):

    def get(self, request, model):
        permiso = PERMISOS_CSV.get(model, None)
        # si no es un modelo permitido 
        if permiso is None:
            raise PermissionDenied
        # si no tiene permiso de verlo
        if not request.user.has_perm(permiso):
            raise PermissionDenied
        # si no es un modelo permitido
        if model not in ALLOWED_MODELS:
            raise PermissionDenied

        deleted = request.GET.get('deleted', None)
        if deleted:
            model_dictionary = ALLOWED_MODELS_DELETED[model]
        else:
            model_dictionary = ALLOWED_MODELS[model]

        queryset = model_dictionary['index'].get_queryset(self)
        # aplica los filtros de la request
        filtered_data = model_dictionary['filter'](self.request.GET, queryset=queryset, request=self.request)
        # obtiene el queryset filtrado
        queryset = filtered_data.qs
        if not queryset.exists():
            messages.error(self.request,'No hay datos para generar el csv')
            return redirect(model_dictionary['page_error'])

        # genera el archivo csv
        generate_csv = model_dictionary['generate_csv']
        virtual_excel = generate_csv(queryset, self.request.user)
        # genera la response
        response = HttpResponse(virtual_excel, content_type='text/csv')
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % model_dictionary['filename']
        # Return the response value
        return response

class GenerateCustomCsv(LoginRequiredMixin, View):

    def get(self, request, model):
        permiso = PERMISOS_CSV.get(model, None)
        # si no es un modelo permitido 
        if permiso is None:
            raise PermissionDenied
        # si no tiene permiso de verlo
        if not request.user.has_perm(permiso):
            raise PermissionDenied
        # si no es un modelo permitido
        if model not in ALLOWED_MODELS:
            raise PermissionDenied

        deleted = request.GET.get('deleted', None)
        if deleted:
            model_dictionary = ALLOWED_MODELS_DELETED[model]
        else:
            model_dictionary = ALLOWED_MODELS[model]

        queryset = model_dictionary['index'].get_queryset(self)
        # aplica los filtros de la request
        filtered_data = model_dictionary['filter'](self.request.GET, queryset=queryset, request=self.request)
        # obtiene el queryset filtrado
        queryset = filtered_data.qs
        if not queryset.exists():
            messages.error(self.request,'No hay datos para generar el csv')
            return redirect(model_dictionary['page_error'])

        # genera el archivo csv
        generate_csv = model_dictionary['generate_csv']
        generate_csv(queryset, self.request.user)
        
        messages.success(self.request, 'El archivo se está generando, se enviará un correo cuando esté listo')

        return redirect(model_dictionary['page_error'])