from apps.dispositivos.views import IndexTagView, IndexCandadoView, IndexGafeteView, IndexGafeteDeletedView, IndexLoteTagView, IndexTagDeletedView
from apps.dispositivos.filters import LoteFilter, CandadoFilter, GafeteFilter, TagFilter
from catalogos_modular.csv_generator import generate_csv_lotes, generate_csv_candados, generate_csv_tags
from .utility.csv_generator import generate_csv_gafetes
from django.urls import reverse_lazy

from .utility.csv_generator import generate_csv_gafetes

PERMISOS_CUSTOM_CSV = {
    'AvisoCruce': 'catalogos_modular.generar_csv_externo',
    'Pedimento': 'catalogos_modular.generar_csv_externo',
    'Gafete': 'gafetes_modular.view_gafetes_index',
    #'Semaforo': 'catalogos_modular.generar_csv_externo',
}

PERMISOS_CSV = {
    'Tag': 'catalogos_modular.view_tags_index',
    'Candado': 'catalogos_modular.view_candados_index',
    'Gafete': 'gafetes_modular.view_gafetes_index',
    'Lote': 'catalogos_modular.view_tags_index',
}

CUSTOM_CSV_CONTEXT = {
    'AvisoCruce': {
        'subject': 'CSV de avisos de cruce',
        'email_content': {
            'modelo': 'avisos de cruce',
        }
    },
    'Pedimento': {
        'subject': 'CSV de pedimentos',
        'email_content': {
            'modelo': 'pedimentos',
        }
    },
    # 'Semaforo': {
    #     'subject': 'CSV de semaforo',
    #     'email_content': {
    #         'modelo': 'semaforo',
    #     }
    # },
}

ALLOWED_MODELS ={
    'Tag': {
        'index': IndexTagView,
        'filter': TagFilter,
        'filename': 'Tags.csv',
        'generate_csv': generate_csv_tags,
        'page_error': reverse_lazy('dispositivos:tags'),
    },
    'Lote': {
        'index': IndexLoteTagView,
        'filter': LoteFilter,
        'filename': 'Lotes.csv',
        'generate_csv': generate_csv_lotes,
        'page_error': reverse_lazy('dispositivos:lotes'),
    },
    'Candado': {
        'index': IndexCandadoView,
        'filter': CandadoFilter,
        'filename': 'Candados.csv',
        'generate_csv': generate_csv_candados,
        'page_error': reverse_lazy('dispositivos:candados'),
    },
    'Gafete': {
        'index': IndexGafeteView,
        'filter': GafeteFilter,
        'filename': 'Gafetes.csv',
        'generate_csv': generate_csv_gafetes,
        'page_error': reverse_lazy('dispositivos:gafetes'),
    },
}

ALLOWED_MODELS_DELETED = {
    'Gafete': {
        'index': IndexGafeteDeletedView,
        'filter': GafeteFilter,
        'filename': 'Gafetes.csv',
        'generate_csv': generate_csv_gafetes,
        'page_error': reverse_lazy('dispositivos:gafetes-deleted'),
    },
    'Tag': {
        'index': IndexTagDeletedView,
        'filter': TagFilter,
        'filename': 'Tags.csv',
        'generate_csv': generate_csv_tags,
        'page_error': reverse_lazy('dispositivos:tags_index_deleted'),
    },
}