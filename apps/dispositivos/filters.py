import django_filters
from catalogos_modular.models import CatalogoCandado, Gafete, Group, Lote, Tag
from django import forms
from django.db.models import Q
from django_filters.widgets import RangeWidget
from gafetes_modular.models import GafeteOficial

BOOLEAN_CHOICES = ((True, 'Si'), (False, 'No'))

def get_groups_tramitadores(request):
    return Group.objects.filter(
        name__in=[ 
            'Tramitador de candados', 
            'Tramitador de tags'
        ]).order_by('name')

class LoteFilter(django_filters.FilterSet):
    created_by__curp = django_filters.CharFilter(label="CURP", widget=forms.TextInput(attrs={'placeholder': 'CURP'}))
    created_by__username = django_filters.CharFilter(label="Usuario", widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    lote = django_filters.CharFilter(label="Lote", widget=forms.TextInput(attrs={'placeholder': 'Lote'}))
    created_by__groups__name = django_filters.ModelChoiceFilter(label="Tipo de usuario", queryset=get_groups_tramitadores)
    class Meta:
        model = Lote
        fields = ['created_by__curp', 'created_by__username', 'lote', 'created_by__groups__name']
    
    def __init__(self, *args, **kwargs):
        super(LoteFilter, self).__init__(*args, **kwargs)
        for field_name in self.get_fields():
            self.filters[field_name].field.widget.attrs.update({'class': 'form-control'})

        self.filters['created_by__curp'].lookup_expr = 'icontains'
        self.filters['created_by__username'].lookup_expr = 'icontains'
        self.filters['lote'].lookup_expr = 'icontains'

class TagFilter(django_filters.FilterSet):
    created_by__curp = django_filters.CharFilter(label="CURP", widget=forms.TextInput(attrs={'placeholder': 'CURP'}))
    lote__lote = django_filters.CharFilter(label="Lote", widget=forms.TextInput(attrs={'placeholder': 'Lote'}))
    tag = django_filters.CharFilter(label="Número de tag", widget=forms.TextInput(attrs={'placeholder': 'Tag'}))
    class Meta:
        model = Tag
        fields = ['created_by__curp', 'tag', 'lote__lote', 'estado']
    
    def __init__(self, *args, **kwargs):
        super(TagFilter, self).__init__(*args, **kwargs)
        for field_name in self.get_fields():
            self.filters[field_name].field.widget.attrs.update({'class': 'form-control'})

            if self.filters[field_name].__class__.__name__ == 'CharFilter':
                self.filters[field_name].lookup_expr = 'icontains'

            if self.filters[field_name].__class__.__name__ == 'ChoiceFilter':
                self.filters[field_name].field.widget.attrs.update({'class': 'form-control form-select'})
        
BOOLEAN_CHOICES = ((True, 'Si'), (False, 'No'))

candado_fields = {
    'candado': {'label': 'Candado'},
    'created_by__curp': {'label': 'CURP'},
    'created_by__username': {'label': 'Usuario'},
    'roto': {'label': 'Roto'},
}

class CandadoFilter(django_filters.FilterSet):
    
    roto = django_filters.ChoiceFilter(label="Roto", choices=BOOLEAN_CHOICES)
    
    class Meta:
        model = CatalogoCandado
        fields = list(candado_fields.keys())
    
    def __init__(self, *args, **kwargs):
        super(CandadoFilter, self).__init__(*args, **kwargs)
        for field_name in self.get_fields():
            label = candado_fields[field_name]['label']
            self.filters[field_name].field.widget.attrs.update({'class': 'form-control', 'placeholder': label})
            self.filters[field_name].field.label = label
            
            if self.filters[field_name].__class__.__name__ == 'CharFilter':
                self.filters[field_name].lookup_expr = 'icontains'

gafete_fields = {
    'numero_gafete': {'label': 'Número de gafete'},
    'numero_gafete_corto': {'label': 'Número de gafete corto'},
    'user__rfc': {'label': 'RFC'},
    'user__tags_id': {'label': 'TAX ID'},
    'user__extranjero': {'label': '¿Es extranjero?'},
    'tipo_gafete': {'label': 'Tipo de gafete'},
    'fecha_vigencia': {'label': 'Fecha de vigencia'},
    'estado': {'label': 'Estado'},
}

class GafeteFilter(django_filters.FilterSet):
    
    fecha_vigencia = django_filters.DateFromToRangeFilter(label="Fecha de vigencia", widget=RangeWidget(attrs={'type': 'date'}))
    user__extranjero = django_filters.ChoiceFilter(choices=BOOLEAN_CHOICES)

    class Meta:
        model = GafeteOficial
        fields = list(gafete_fields.keys())
    
    def __init__(self, *args, **kwargs):
        super(GafeteFilter, self).__init__(*args, **kwargs)
        for field_name in self.get_fields():
            label = gafete_fields[field_name]['label']
            self.filters[field_name].field.widget.attrs.update({'class': 'form-control', 'placeholder': label})
            self.filters[field_name].field.label = label
            
            if self.filters[field_name].__class__.__name__ == 'CharFilter':
                self.filters[field_name].lookup_expr = 'icontains'