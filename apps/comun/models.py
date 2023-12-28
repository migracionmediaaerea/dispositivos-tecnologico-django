from django.db import models
from safedelete.models import SafeDeleteModel
from simple_history.models import HistoricalRecords


# Create your models here.
class AbstractModel(SafeDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('catalogos_modular.User', related_name='+', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey('catalogos_modular.User',  related_name='+', on_delete=models.DO_NOTHING, null=True)
    history = HistoricalRecords(inherit=True)
    
    class Meta:
        abstract = True


class AbstractNullableModel(SafeDeleteModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('catalogos_modular.User', related_name='+', on_delete=models.DO_NOTHING, null=True)
    updated_by = models.ForeignKey('catalogos_modular.User',  related_name='+', on_delete=models.DO_NOTHING, null=True)
    history = HistoricalRecords(inherit=True)
    
    class Meta:
        abstract = True